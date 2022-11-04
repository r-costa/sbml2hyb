from xml.etree import ElementTree as ET
import sys
from xml.etree.ElementTree import tostring
from libsbml import *

from sbml2hyb.xml_validator import validate_sbml


def translate_mathml(xml):
    """
    Translates the MathML formula to text
    :param xml: The MathML formula
    :return:
    """
    math = readMathMLFromString(xml)
    return formulaToString(math)


def translate_rule_math(rule):
    """
    Translates a MathML rule and returns it as text
    :param rule: The MathML formula
    :return:
    """
    if rule.isSetMath():
        formula = formulaToString(rule.getMath())

        if len(rule.getVariable()) > 0:
            return formula
        else:
            return formula + " = 0"
    else:
        return "Undefined"


def translate_reaction_math(reaction):
    """
    Translates a MathML reaction and returns it as text
    :param reaction: The MathML formula
    :return:
    """
    if reaction.isSetKineticLaw():
        kl = reaction.getKineticLaw()
        if kl.isSetMath():
            formula = formulaToString(kl.getMath())
            return formula
        else:
            return "Undefined"
    else:
        return "Undefined"


def translate_event_assignment_math(event_assignement):
    """
    Translates a MathML event assignment and returns it as text
    :param event_assignement: The MathML formula
    :return:
    """
    if event_assignement.isSetMath():
        formula = formulaToString(event_assignement.getMath())
        return formula
    else:
        return "Undefined"


def translate_event_delay_math(event):
    """
    Translates a MathML event delay and returns it as text
    :param event: The MathML formula
    :return:
    """
    if event.isSetDelay():
        formula = formulaToString(event.getDelay().getMath())
        return formula
    else:
        return "Undefined"


def translate_event_trigger_math(event):
    """
    Translates a MathML event trigger and returns it as text
    :param event: The MathML formula
    :return:
    """
    if event.isSetTrigger():
        formula = formulaToString(event.getTrigger().getMath())
        return formula
    else:
        return "Undefined"


def write_species(root, namespace, filename):
    """
    Analyzes the <species> elements in the <listOfSpecies> and builds the hmod corresponding strings
    :param root: The xml root
    :param namespace: The sbml namespace
    :param filename: The name of the file
    :return: The hmod species strings
    """
    species_for_hmod = []

    species_string = "\n"
    species_string += "% Species\n"

    species = root.findall("./*/{{{}}}listOfSpecies/*".format(namespace))
    species_string += "{}.nspecies={};\n".format(filename, len(species))
    for i, specie in enumerate(species):
        count = i + 1

        # specie id
        if "id" in specie.attrib:
            species_for_hmod.append("{}".format(specie.attrib["id"]))
            species_string += '{}.species({}).id="{}";\n'.format(
                filename, count, specie.attrib["id"]
            )

        # specie val
        if "initialConcentration" in specie.attrib:
            species_string += "{}.species({}).val={};\n".format(
                filename, count, specie.attrib["initialConcentration"]
            )

        # specie compartment
        if "compartment" in specie.attrib:
            species_string += '{}.species({}).compartment="{}";\n'.format(
                filename, count, specie.attrib["compartment"]
            )

        # specie fixed
        if "constant" in specie.attrib:
            species_string += "{}.species({}).fixed={};\n".format(
                filename, count, 0 if specie.attrib["constant"] == "false" else 1
            )
        else:
            species_string += "{}.species({}).fixed={};\n".format(filename, count, 0)

        # specie min
        species_string += "{}.species({}).min={};\n".format(filename, count, 0)

        # specie max
        species_string += "{}.species({}).max={};\n".format(filename, count, 15)

        # specie isres
        species_string += "{}.species({}).isres={};\n".format(filename, count, 1)

    return [species_string, species_for_hmod]


def write_compartments(root, namespace, filename):
    """
    Analyzes the <compartment> elements in the <listOfCompartments> and builds the hmod corresponding strings
    :param root: The xml root
    :param namespace: The sbml namespace
    :param filename: The name of the file
    :return: The hmod compartments strings
    """
    compartments_string = "\n"
    compartments_string += "% Compartments\n"
    compartments = root.findall("./*/{{{}}}listOfCompartments/*".format(namespace))
    compartments_string += "{}.ncompartments={};\n".format(filename, len(compartments))

    for i, compartment in enumerate(compartments):
        count = i + 1

        # compartment id
        if "id" in compartment.attrib:
            compartments_string += '{}.compartments({}).id="{}";\n'.format(
                filename, count, compartment.attrib["id"]
            )

        # compartment val
        if "size" in compartment.attrib:
            compartments_string += "{}.compartments({}).val={};\n".format(
                filename, count, compartment.attrib["size"]
            )

        # compartment fixed
        if "constant" in compartment.attrib:
            compartments_string += "{}.compartments({}).fixed={};\n".format(
                filename, count, 0 if compartment.attrib["constant"] == "false" else 1
            )
        else:
            compartments_string += "{}.compartments({}).fixed={};\n".format(
                filename, count, 0
            )

        # compartment min
        compartments_string += "{}.compartments({}).min={};\n".format(
            filename, count, 0
        )

        # compartment max
        compartments_string += "{}.compartments({}).max={};\n".format(
            filename, count, 15
        )

        # compartment isres
        compartments_string += "{}.compartments({}).isres={};\n".format(
            filename, count, 0
        )

    return compartments_string


def write_parameters(root, namespace, filename):
    """
    Analyzes the <parameter> elements in the <listOfParameters> and builds the hmod corresponding strings
    :param root: The xml root
    :param namespace: The sbml namespace
    :param filename: The name of the file
    :return: The hmod parameters strings
    """
    parameters_for_hmod = []
    parameters_string = "\n"
    parameters_string += "% Parameters\n"
    parameters = root.findall("./*/{{{}}}listOfParameters/*/[@id]".format(namespace))
    local_parameters = root.findall(
        "./*/{{{}}}listOfReactions/*/{{{}}}kineticLaw/{{{}}}listOfParameters/*".format(
            namespace, namespace, namespace
        )
    )
    local_parameters += root.findall(
        "./*/{{{}}}listOfReactions/*/{{{}}}kineticLaw/{{{}}}listOfLocalParameters/*".format(
            namespace, namespace, namespace
        )
    )
    aux = []
    for i, local_parameter in enumerate(local_parameters):
        can_be_inputted = True
        for j in range(len(aux)):
            if "id" in aux[j].attrib and "id" in local_parameter.attrib:
                if aux[j].attrib["id"] == local_parameter.attrib["id"]:
                    can_be_inputted = False
                    break
        if can_be_inputted:
            aux.append(local_parameter)

    local_parameters = aux
    number_of_local_parameters = 0
    for i, local_parameter in enumerate(local_parameters):
        # if parameter.attrib["value"] == "0":
        #     continue

        # Check if parameter is Global
        is_local = True
        for j, parameter in enumerate(parameters):
            if "id" in local_parameter.attrib and "id" in parameter.attrib:
                if parameter.attrib["id"] == local_parameter.attrib["id"]:
                    is_local = False
                    break
        if not is_local:
            continue
        number_of_local_parameters += 1

    parameters_string += "{}.nparameters={};\n".format(
        filename, number_of_local_parameters + len(parameters)
    )
    param_counter = 0

    for i, parameter in enumerate(parameters):
        # if parameter.attrib["value"] == "0":
        #     continue

        param_counter += 1
        # parameter id
        if "id" in parameter.attrib:
            parameters_for_hmod.append("{}".format(parameter.attrib["id"]))
            parameters_string += '{}.parameters({}).id="{}";\n'.format(
                filename, param_counter, parameter.attrib["id"]
            )

        # parameter val
        if "value" in parameter.attrib:
            parameters_string += "{}.parameters({}).val={};\n".format(
                filename, param_counter, parameter.attrib["value"]
            )

        # parameter fixed
        if "constant" in parameter.attrib:
            parameters_string += "{}.parameters({}).fixed={};\n".format(
                filename,
                param_counter,
                0 if parameter.attrib["constant"] == "false" else 1,
            )
        else:
            parameters_string += "{}.parameters({}).fixed={};\n".format(
                filename, param_counter, 0
            )

        # parameter reaction
        parameters_string += '{}.parameters({}).reaction="{}";\n'.format(
            filename, param_counter, "global"
        )

    for local_parameter in local_parameters:

        # Check if parameter is in Local
        is_global = False
        for j, global_parameter in enumerate(parameters):
            if "id" in local_parameter.attrib and "id" in global_parameter.attrib:
                if local_parameter.attrib["id"] == global_parameter.attrib["id"]:
                    is_global = True
                    break
        if is_global:
            continue

        param_counter += 1
        # local parameter id
        if "id" in local_parameter.attrib:
            parameters_for_hmod.append("{}".format(local_parameter.attrib["id"]))
            parameters_string += '{}.parameters({}).id="{}";\n'.format(
                filename, param_counter, local_parameter.attrib["id"]
            )

        # local parameter val
        if "value" in local_parameter.attrib:
            parameters_string += "{}.parameters({}).val={};\n".format(
                filename, param_counter, local_parameter.attrib["value"]
            )

        # parameter fixed
        if "constant" in local_parameter.attrib:
            parameters_string += "{}.parameters({}).fixed={};\n".format(
                filename,
                param_counter,
                0 if local_parameter.attrib["constant"] == "false" else 1,
            )
        else:
            parameters_string += "{}.parameters({}).fixed={};\n".format(
                filename, param_counter, 0
            )

        # local parameter reaction
        parameters_string += '{}.parameters({}).reaction="{}";\n'.format(
            filename, param_counter, "local"
        )

    return [parameters_string, parameters_for_hmod]


def write_assignment_rules(root, namespace, filename):
    """
    Analyzes the <assignmentRule> elements in the <listOfRules> and builds the hmod corresponding strings
    :param root: The xml root
    :param namespace: The sbml namespace
    :param filename: The name of the file
    :return: The hmod assignmentRule strings
    """

    assignment_rules_string = "\n"
    assignment_rules_string += "% Assignment rules\n"
    ruleAss = root.findall(
        "./*/{{{}}}listOfRules/{{{}}}assignmentRule".format(namespace, namespace)
    )
    assignment_rules_string += "{}.nruleAss={};\n".format(filename, len(ruleAss))

    for i, assignment_rule in enumerate(ruleAss):
        count = i + 1

        # assignment_rule id
        if "variable" in assignment_rule.attrib:
            assignment_rules_string += '{}.ruleAss({}).id="{}";\n'.format(
                filename, count, assignment_rule.attrib["variable"]
            )

        # assignment_rule val
        # val = translate_mathml(assignment_rule.find(
        #     './{http://www.w3.org/1998/Math/MathML}math/*'))
        rule = tostring(
            assignment_rule.find("./{http://www.w3.org/1998/Math/MathML}math"),
            encoding="unicode",
            method="xml",
        )
        val = translate_mathml(rule)
        assignment_rules_string += '{}.ruleAss({}).val="{}";\n'.format(
            filename, count, val
        )

    return assignment_rules_string


def write_events(root, namespace, filename):
    """
    Analyzes the <event> elements in the <listOfEvents> and builds the hmod corresponding strings
    :param root: The xml root
    :param namespace: The sbml namespace
    :param filename: The name of the file
    :return: The hmod events strings
    """

    events_string = "\n"
    events_string += "% Events\n"
    events = root.findall("./*/{{{}}}listOfEvents/*".format(namespace))
    events_string += "{}.nevents={};\n".format(filename, len(events))

    for i, event in enumerate(events):
        count = i + 1

        # event id
        events_string += '{}.events({}).id="{}";\n'.format(
            filename, count, "Controller"
        )

        # event trigger
        # trigger = translate_mathml(event.find(
        #     './{{{}}}trigger/{{http://www.w3.org/1998/Math/MathML}}math/*'.format(namespace)))
        math_trigger = tostring(
            event.find(
                "./{{{}}}trigger/{{http://www.w3.org/1998/Math/MathML}}math".format(
                    namespace
                )
            ),
            encoding="unicode",
            method="xml",
        )
        trigger = translate_mathml(math_trigger)

        events_string += '{}.events({}).trigger="{}";\n'.format(
            filename, count, trigger
        )

        # event delay
        math_delay = tostring(
            event.find(
                "./{{{}}}delay/{{http://www.w3.org/1998/Math/MathML}}math".format(
                    namespace
                )
            ),
            encoding="unicode",
            method="xml",
        )
        delay = translate_mathml(math_delay)
        events_string += '{}.events({}).delay="{}";\n'.format(filename, count, delay)

        event_assignements = event.findall(
            "./{{{}}}listOfEventAssignments/*".format(namespace)
        )

        for j, event_assignement in enumerate(event_assignements):
            ass_count = j + 1

            # event assignement var
            if "variable" in event_assignement.attrib:
                events_string += '{}.events({}).var({})="{}";\n'.format(
                    filename, count, ass_count, event_assignement.attrib["variable"]
                )

            # event assignement var
            # var = translate_mathml(event_assignement.find(
            #     './{http://www.w3.org/1998/Math/MathML}math/*'))
            math_var = tostring(
                event_assignement.find("./{http://www.w3.org/1998/Math/MathML}math"),
                encoding="unicode",
                method="xml",
            )
            var = translate_mathml(math_var)
            events_string += '{}.events({}).var({})="{}";\n'.format(
                filename, count, ass_count, var
            )

    return events_string


def write_reactions(root, namespace, filename):
    """
    Analyzes the <reaction> elements in the <listOfReactions> and builds the hmod corresponding strings
    :param root: The xml root
    :param namespace: The sbml namespace
    :param filename: The name of the file
    :return: The hmod reaction strings
    """

    reactions_string = "\n"
    reactions_string += "% Reactions\n"
    reactions = root.findall("./*/{{{}}}listOfReactions/*".format(namespace))
    reactions_string += "{}.nreaction={};\n".format(filename, len(reactions))

    species = root.findall("./*/{{{}}}listOfSpecies/*".format(namespace))
    species_list = []
    for specie in species:
        if "id" in specie.attrib:
            species_list += [specie.attrib["id"]]

    for i, reaction in enumerate(reactions):
        count = i + 1
        # reaction id
        if "id" in reaction.attrib:
            reactions_string += '{}.reaction({}).id="{}";\n'.format(
                filename, count, reaction.attrib["id"]
            )

        # reaction rate
        # rate = translate_mathml(reaction.find(
        #     './{{{}}}kineticLaw/{{http://www.w3.org/1998/Math/MathML}}math/*'.format(namespace)))
        # reactions_string += ('{}.reaction({}).rate="{}";\n'.format(filename, count, rate))
        # rate = translate_reaction_math(model.getReaction(i))
        math_rate = tostring(
            reaction.find(
                "./{{{}}}kineticLaw/{{http://www.w3.org/1998/Math/MathML}}math".format(
                    namespace
                )
            ),
            encoding="unicode",
            method="xml",
        )
        rate = translate_mathml(math_rate)
        reactions_string += '{}.reaction({}).rate="{}";\n'.format(filename, count, rate)

        values = {k: "0" for k in species_list}
        reactants_list = reaction.findall("./{{{}}}listOfReactants/*".format(namespace))
        reactants_dict = {
            k.attrib["species"]: k.attrib["stoichiometry"]
            if "stoichiometry" in k.attrib
            else "1"
            for k in reactants_list
        }

        products_list = reaction.findall("./{{{}}}listOfProducts/*".format(namespace))
        products_dict = {
            k.attrib["species"]: k.attrib["stoichiometry"]
            if "stoichiometry" in k.attrib
            else "1"
            for k in products_list
        }

        for j in reactants_dict:
            values[j] = "-" + reactants_dict[j] if reactants_dict[j] != "0" else "0"
        for j in products_dict:
            values[j] = products_dict[j]

        # reaction values
        reactions_string += '{}.reaction({}).{}="{}";\n'.format(
            filename, count, reaction.attrib["id"], list(values.values())
        )

    return reactions_string


def write_rate_rules(root, namespace, filename):
    """
    Analyzes the <rateRule> elements in the <listOfRules> and builds the hmod corresponding strings
    :param root: The xml root
    :param namespace: The sbml namespace
    :param filename: The name of the file
    :return: The hmod rateRules strings
    """

    rate_rules_string = "\n"
    rate_rules_string += "% Rate rules\n"
    rateRules = root.findall(
        "./*/{{{}}}listOfRules/{{{}}}rateRule".format(namespace, namespace)
    )
    rate_rules_string += "{}.nraterules={};\n".format(filename, len(rateRules))

    for i, rate_rule in enumerate(rateRules):
        count = i + 1
        # assignment_rule id
        if "variable" in rate_rule.attrib:
            rate_rules_string += '{}.raterules({}).id="{}";\n'.format(
                filename, count, rate_rule.attrib["variable"]
            )

        # assignment_rule val
        # val = translate_mathml(rate_rule.find(
        #     './{http://www.w3.org/1998/Math/MathML}math/*'))

        rule = tostring(
            rate_rule.find("./{http://www.w3.org/1998/Math/MathML}math"),
            encoding="unicode",
            method="xml",
        )
        val = translate_mathml(rule)

        rate_rules_string += '{}.raterules({}).val="{}";\n'.format(filename, count, val)

        # compartment min
        rate_rules_string += "{}.raterules({}).min={};\n".format(filename, count, 0)

        # compartment max
        rate_rules_string += "{}.raterules({}).max={};\n".format(filename, count, 1.5)

        # compartment isres
        rate_rules_string += "{}.raterules({}).isres={};\n".format(filename, count, 0)

    return rate_rules_string


def main(filename, file_string):
    a = validate_sbml(file_string)
    if a != 0:
        return [
            "The SBML file is not valid. See the reason(s) below: \n\n\n" + a,
            None,
            None,
        ]

    # parsing the xml
    tree = ET.fromstring(file_string)  # open(filename))
    # getting the xml root
    root = tree

    # getting the sbml namespace
    namespace = root.tag.replace("{", "").replace("}sbml", "")

    # building the hmod filename, wich is the same as the xml one
    if ".xml" in filename:
        hmod_filename = filename.split("/")[-1].replace(".xml", "")
    else:
        hmod_filename = filename.split("/")[-1].replace(".hmod", "")

    # building the hmod file string
    f = "% --------------------------------------------------------------------------\n"
    # f += ("% hybrid model definition data structure\n")
    f += "% hmod model structure\n"
    res = write_species(root, namespace, hmod_filename)
    species = res[1]
    f += res[0]
    f += write_compartments(root, namespace, hmod_filename)
    res = write_parameters(root, namespace, hmod_filename)
    parameters = res[1]
    f += res[0]
    f += write_assignment_rules(root, namespace, hmod_filename)
    f += write_events(root, namespace, hmod_filename)
    f += write_reactions(root, namespace, hmod_filename)
    f += write_rate_rules(root, namespace, hmod_filename)
    f += "\n"
    f += "\n"
    f += "end"

    return [f, species, parameters]


if __name__ == "__main__":
    # calling main function
    if len(sys.argv) != 2:
        print("Usage: python xml_parser.py 'filename'")
    else:
        file = sys.argv[1]
        main(file)
