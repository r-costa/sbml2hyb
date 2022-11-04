import os
import sys
from xml.etree import ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import fromstring, register_namespace
import ast
from libsbml import *

from sbml2hyb.Hmod import Hmod
from sbml2hyb.hmod_validator import validate_hmod

meta_id = 0


def build_xml_string(sbml):
    """
    Builds the sbml string of the file
    :param sbml: The xml root element
    :return:
    """

    # builds the string file with proper identation
    xmlstr = minidom.parseString(
        ET.tostring(sbml, xml_declaration=True, encoding="UTF-8")
    ).toprettyxml(indent="\t", encoding="UTF-8")

    # necessary adjustments to make the produced file cleaner
    string_to_write = (
        xmlstr.decode("utf-8")
        .replace(' xmlns:math="http://www.w3.org/1998/Math/MathML"', "")
        .replace("<math:math", '<math xmlns="http://www.w3.org/1998/Math/MathML"')
        .replace("math:", "")
        .replace(
            "<ci> time </ci>",
            '<csymbol encoding="text" definitionURL="http://www.sbml.org/sbml/symbols/time"> time </csymbol>',
        )
        .replace(
            "<ci> t </ci>",
            '<csymbol encoding="text" definitionURL="http://www.sbml.org/sbml/symbols/time"> time </csymbol>',
        )
    )

    # removing empty lines
    string_to_write = "".join(
        [s for s in string_to_write.strip().splitlines(True) if s.strip()]
    )
    return string_to_write


def get_parameters(lines):
    """
    Returns the global parameters in hmod strings
    :param lines: The file string lines
    :return:
    """
    parameters = []
    for i in lines:
        if "parameters(" in i:
            parameters += [i]
    return parameters


def get_local_parameters(lines):
    """
    Returns the global parameters in hmod strings
    :param lines: The file string lines
    :return:
    """
    parameters = []
    for i in lines:
        if "parameters(" in i:
            parameters += [i]
        if "global" in i:
            parameters = parameters[: len(parameters) - 4]
    return parameters


def get_global_parameters(lines):
    """
    Returns the global parameters in hmod strings
    :param lines: The file string lines
    :return:
    """
    parameters = []
    for i in lines:
        if "parameters(" in i:
            parameters += [i]
        if "local" in i:
            parameters = parameters[: len(parameters) - 4]
    return parameters


def get_local_parameters_dict(lines):
    """
    Returns a dict with {"parameter": parameter value}
    :param lines: The file string lines
    :return:
    """
    global_parameters = get_global_parameters(lines)

    par = [
        get_value_from_string(i)
        for i in lines
        if "parameters(" in i and "id" in i and i not in global_parameters
    ]
    par_values = [
        get_value_from_string(i)
        for i in lines
        if "parameters(" in i and "val" in i and i not in global_parameters
    ]
    param_dict = {param: par_values[i] for i, param in enumerate(par)}
    return param_dict


def get_value_from_string(string):
    """
    Returns the desired attribute value from an hmod string
    :param string: The whole string
    :return:
    """
    return str(string.split("=")[-1].replace('"', "").replace(";", "").replace("'", ""))


def translateInfix(formula):
    """
    Translates the text formula to MathML
    :param formula:
    :return: The MathML
    """
    math = parseFormula(formula)
    return writeMathMLToString(math)


def get_attribute_list(lines, category, category_number):
    """
    Returns the attribute list for a certain category
    Example for an assignment rule:

    Park_SBML.nruleAss=1;
    Park_SBML.ruleAss(1).id="D";
    Park_SBML.ruleAss(1).val="Feed / V";

    Is converted to the list ["D", "Feed / V"]

    :param lines: File string lines
    :param category: The string representing the hmod category
    :param category_number: The number of attributes the category has
    :return:
    """
    # collect every string related to the category
    attributes_list = [get_value_from_string(i) for i in lines if category in i]

    # divides all category attributes into multiple lists to process each one separately
    #
    # For compartments list:
    # for example, for a file with 2 compartments, x would be:
    # [
    # ['V', '1', '0', '15', '0'],
    # ['H', '1', '0', '15', '0'],
    # ]
    # Being the order: [id, val, fixed, min, max]
    x = [
        attributes_list[i : i + category_number]
        for i in range(0, len(attributes_list), category_number)
    ]
    return x


def store_compartments(compartments, list_of_compartments):
    """
    Produces the <listOfCompartments>
    :param compartments: A list with all compartments attributes
    :param list_of_compartments: The xml element
    """
    global meta_id

    # processing each compartment
    for i in compartments:
        compartment = ET.SubElement(
            list_of_compartments,
            "compartment",
            metaid="metaid_" + str(meta_id),
            id=i[0],
            size=i[1],
            constant="false" if i[2] == "0" else "true",
        )
        meta_id += 1


def store_species(species, list_of_species):
    """
    Produces the <listOfSpecies>
    :param species: A list with all species attributes
    :param list_of_species: The xml element
    """
    global meta_id

    # processing each species
    for i in species:
        specie = ET.SubElement(
            list_of_species,
            "species",
            metaid="metaid_" + str(meta_id),
            id=i[0],
            compartment=i[2],
            initialConcentration=i[1],
            constant="false" if i[3] == "0" else "true",
        )
        meta_id += 1


def store_parameters(lines, list_of_parameters):
    """
    Produces the <listOfParameters>
    :param lines: The file string lines
    :param list_of_parameters: The xml element
    :return id list of parameters
    """
    global meta_id

    # collect every string related to parameters
    parameters = get_global_parameters(lines)  # + get_local_parameters(lines)

    # the number of attributes that a parameter has in hmod
    parameters_number = 4

    # divides all parameters into multiple lists to process each one separately
    x = [
        parameters[i : i + parameters_number]
        for i in range(0, len(parameters), parameters_number)
    ]

    list_of_ids = []
    # processing each parameter
    for i in x:
        cur_id = get_value_from_string(i[0])
        list_of_ids.append(cur_id)
        parameter = ET.SubElement(
            list_of_parameters,
            "parameter",
            metaid="metaid_" + str(meta_id),
            id=cur_id,
            value=get_value_from_string(i[1]),
            constant="false" if get_value_from_string(i[2]) == "0" else "true",
        )
        meta_id += 1

    local_params = get_local_parameters_dict(lines)
    for key in local_params.keys():
        list_of_ids.append(key)

    return list_of_ids


def store_rate_rules(rate_rules, list_of_rate_rules):
    """
    Produces all the <rateRule> elements in a <listOfRules>
    :param rate_rules: A list with all rate rules attributes
    :param list_of_rate_rules: The xml element
    """
    global meta_id

    # processing each rate rule
    for i in rate_rules:
        compartment = ET.SubElement(
            list_of_rate_rules,
            "rateRule",
            metaid="metaid_" + str(meta_id),
            variable=i[0],
        )

        # builds the MathML
        equation = i[1]
        eq = fromstring(
            translateInfix(equation).replace(
                '<?xml version="1.0" encoding="UTF-8"?>', ""
            )
        )
        compartment.append(eq)
        meta_id += 1


def store_assignment_rules(assignment_rules, list_of_assignment_rules):
    """
    Produces all the <assignmentRule> elements in a <listOfRules>
    :param assignment_rules: A list with all assignment rules attributes
    :param list_of_assignment_rules: The xml element
    """

    global meta_id

    # processing each assignment rule
    for i in assignment_rules:
        assignment_rule = ET.SubElement(
            list_of_assignment_rules,
            "assignmentRule",
            metaid="metaid_" + str(meta_id),
            variable=i[0],
        )

        # builds the MathML
        equation = i[1]
        eq = fromstring(
            translateInfix(equation).replace(
                '<?xml version="1.0" encoding="UTF-8"?>', ""
            )
        )
        assignment_rule.append(eq)
        meta_id += 1


def store_reactions(lines, list_of_reactions, species_list):
    """
    Produces the <listOfReactions>
    :param lines: The file string lines
    :param list_of_reactions: The xml element
    :param species_list: The string list of all species
    """
    global meta_id

    # collect every string related to reactions
    reactions = [i for i in lines if "reaction(" in i]

    # the number of attributes that a reaction has in hmod
    reactions_number = 3

    # divides all reactions into multiple lists to process each one separately
    x = [
        reactions[i : i + reactions_number]
        for i in range(0, len(reactions), reactions_number)
    ]

    # processing each reaction
    for i in x:

        reaction = ET.SubElement(
            list_of_reactions,
            "reaction",
            metaid="metaid_" + str(meta_id),
            id=get_value_from_string(i[0]),
        )
        meta_id += 1

        # Transforming a string containing a list with the stoichiometric values into a proper list of strings
        # e.g. The string "['1', '2', '3', '4']" into the list ['1', '2', '3', '4']
        x = ast.literal_eval(get_value_from_string(i[2]))

        # converting the stoichiometric string values into floats
        species_values = [float(k) for k in x]

        # list of products dict, with the key being the specie index in the spceies_list, and the corresponding
        # stoichiometric value
        products = {}

        # list of reactants dict, with the key being the specie index in the spceies_list, and the corresponding
        # stoichiometric value
        reactants = {}

        # filling the products and reactants dicts
        # if the specie as a stoichiometric value equal to 0 it does not participate in the reaction
        # if the specie as a stoichiometric value lesser than 0 it is a reactant
        # if the specie as a stoichiometric value greater than 0 it is a product
        for j, value in enumerate(species_values):
            if value < 0:
                reactants[j] = abs(value)
            elif value > 0:
                products[j] = value

        # if there are any reactants, builds the <listOfReactants>
        if len(reactants) > 0:
            listOfReactants = ET.SubElement(reaction, "listOfReactants")
            # building each <speciesReference>
            for key, value in reactants.items():
                speciesReference = ET.SubElement(
                    listOfReactants,
                    "speciesReference",
                    metaid="metaid_" + str(meta_id),
                    species=species_list[key],
                    stoichiometry=str(value),
                )
                meta_id += 1

        # if there are any products, builds the <listOfProducts>
        if len(products) > 0:
            listOfProducts = ET.SubElement(reaction, "listOfProducts")
            # building each <speciesReference>
            for key, value in products.items():
                speciesReference = ET.SubElement(
                    listOfProducts,
                    "speciesReference",
                    metaid="metaid_" + str(meta_id),
                    species=species_list[key],
                    stoichiometry=str(value),
                )
                meta_id += 1

        # Builds the MathML
        equation = get_value_from_string(i[1])
        eq = fromstring(
            translateInfix(equation).replace(
                '<?xml version="1.0" encoding="UTF-8"?>', ""
            )
        )

        # searching for all <modifierSpeciesReference> elements of <listOfModifiers>
        # if it is a product or reactant, then is added
        # if it is referenced in the MathML it is added, as long as it is a species
        modifiers = [
            i.text.strip()
            for i in eq.findall(".//{http://www.w3.org/1998/Math/MathML}ci")
            if i.text.strip() in species_list
        ]
        modifiers = [m for m in modifiers if m != ""]
        modifiers += [species_list[i] for i in products]
        modifiers += [species_list[i] for i in reactants]
        modifiers = list(dict.fromkeys(modifiers))

        # building the <listOfModifiers> xml element
        listOfModifiers = ET.SubElement(reaction, "listOfModifiers")

        # processing each modifier
        for modifier in modifiers:
            modifierSpeciesReference = ET.SubElement(
                listOfModifiers,
                "modifierSpeciesReference",
                metaid="metaid_" + str(meta_id),
                species=modifier,
            )
            meta_id += 1

        # finally appends the MathMl to the <kineticLaw>
        kineticLaw = ET.SubElement(reaction, "kineticLaw")
        kineticLaw.append(eq)

        # finding the local parameters of a kinetic law
        # store all the elements that are inside a <ci> and are local parameters
        local_parameters = get_local_parameters_dict(lines)
        parameters = [
            i.text.strip()
            for i in eq.findall(".//{http://www.w3.org/1998/Math/MathML}ci")
            if i.text.strip() in local_parameters
        ]

        # removing duplicates
        parameters = list(set(parameters))

        # remove global
        global_parameters = get_global_parameters(lines)
        aux = [
            global_parameters[i : i + 4] for i in range(0, len(global_parameters), 4)
        ]
        final_parameters = []
        for parameter in parameters:
            is_global = False
            for i in aux:
                cur_id = get_value_from_string(i[0])
                if parameter == cur_id:
                    is_global = True
                    break
            if not is_global:
                final_parameters.append(parameter)

        parameters = final_parameters
        # adding the parameters
        if len(parameters) > 0:
            listOfParameters = ET.SubElement(kineticLaw, "listOfParameters")
            for param in parameters:
                parameter = ET.SubElement(
                    listOfParameters,
                    "parameter",
                    metaid="metaid_" + str(meta_id),
                    id=param,
                    value=local_parameters[param],
                )
                meta_id += 1


def store_events(events, list_of_events):
    """
    Produces the <listOfEvents>
    :param events: A list with all events attributes
    :param list_of_events: The xml element
    """
    global meta_id

    # # collect every string related to reactions
    # events = [i for i in lines if "events(" in i]
    #
    # # the number of attributes that an event has in hmod
    # events_number = 5
    #
    # # divides all events into multiple lists to process each one separately
    # x = [events[i:i + events_number] for i in range(0, len(events), events_number)]

    # processing each event
    for i in events:
        event = ET.SubElement(list_of_events, "event", metaid="metaid_" + str(meta_id))

        # builds the <trigger> element
        trigger = ET.SubElement(event, "trigger")
        trigger_equation = get_value_from_string(i[1])
        eq = fromstring(
            translateInfix(trigger_equation).replace(
                '<?xml version="1.0" encoding="UTF-8"?>', ""
            )
        )
        trigger.append(eq)

        # builds the <delay> element
        delay = ET.SubElement(event, "delay")
        delay_equation = get_value_from_string(i[2])
        eq = fromstring(
            translateInfix(delay_equation).replace(
                '<?xml version="1.0" encoding="UTF-8"?>', ""
            )
        )
        delay.append(eq)

        meta_id += 1

        # builds the <listOfEventAssignments> for this event
        store_event_assignments(event, i[3:])


def store_event_assignments(event, event_assignments):
    """
    Produces the <listOfEventAssignments> for an <event>
    :param event: The event
    :param event_assignments: The string lines containing the event assignments attributes
    :return:
    """
    # building the <listOfEventAssignments> xml element
    listOfEventAssignments = ET.SubElement(event, "listOfEventAssignments")

    # the number of attributes that an event assignment has in hmod
    event_assignments_number = 2

    # divides all event assignments into multiple lists to process each one separately
    x = [
        event_assignments[i : i + event_assignments_number]
        for i in range(0, len(event_assignments), event_assignments_number)
    ]

    # processing each event assignment
    for i in x:
        event_assignment = ET.SubElement(
            listOfEventAssignments,
            "eventAssignment",
            metaid="metaid_" + str(meta_id),
            variable=get_value_from_string(i[0]),
        )

        # builds the MathML
        event_assignment_equation = get_value_from_string(i[1])
        eq = fromstring(
            translateInfix(event_assignment_equation).replace(
                '<?xml version="1.0" encoding="UTF-8"?>', ""
            )
        )
        event_assignment.append(eq)


def main(filename, doc):

    lines = doc.split("\n")

    # Strips the newline character
    for count, line in enumerate(lines):
        lines[count] = line.strip()
        count += 1
    hmod_valid = validate_hmod(lines)
    if hmod_valid != 0:
        return [hmod_valid, None, None]

    # resgister the mathml namespace
    register_namespace("math", "http://www.w3.org/1998/Math/MathML")

    # build the <sbml>
    sbml = ET.Element(
        "sbml", xmlns="http://www.sbml.org/sbml/level2/version4", level="2", version="4"
    )

    # build the <model>
    model = ET.SubElement(
        sbml,
        "model",
        id=(
            filename.split("/")[-1].replace(".hmod", "")
            if ".hmod" in filename
            else filename.split("/")[-1].replace(".xml", "")
        ),
    )

    # builds the <listOfCompartments>
    compartments_number = 6
    compartments = get_attribute_list(lines, "compartments(", compartments_number)
    if compartments:
        listOfCompartments = ET.SubElement(model, "listOfCompartments")
        store_compartments(compartments, listOfCompartments)

    # builds the <listOfSpecies>
    species_number = 7
    species = get_attribute_list(lines, "species(", species_number)
    if species:
        listOfSpecies = ET.SubElement(model, "listOfSpecies")
        store_species(species, listOfSpecies)

    # builds the <listOfParameters>
    listOfParameters = ET.SubElement(model, "listOfParameters")
    p = store_parameters(lines, listOfParameters)

    # builds the <listOfRules>

    rate_rules_number = 5
    rate_rules = get_attribute_list(lines, "raterules(", rate_rules_number)
    assignment_rules_number = 2
    assignment_rules = get_attribute_list(lines, "ruleAss(", assignment_rules_number)

    if rate_rules or assignment_rules:
        listOfRules = ET.SubElement(model, "listOfRules")

    if rate_rules:
        store_rate_rules(rate_rules, listOfRules)

    if assignment_rules:
        store_assignment_rules(assignment_rules, listOfRules)

    # builds the <listOfReactions>
    listOfReactions = ET.SubElement(model, "listOfReactions")
    species = [i.attrib["id"] for i in sbml.findall("./*/listOfSpecies/*")]
    store_reactions(lines, listOfReactions, species)

    # builds the <listOfEvents>
    events_number = 5
    events = get_attribute_list(lines, "events(", events_number)
    if events:
        listOfEvents = ET.SubElement(model, "listOfEvents")
        store_events(events, listOfEvents)

    global meta_id
    meta_id = 0

    return [build_xml_string(sbml), species, p]


if __name__ == "__main__":
    # calling main function
    if len(sys.argv) != 2:
        print("Usage: python xml_parser.py 'filename'")
    else:
        file = sys.argv[1]
        main(file)
