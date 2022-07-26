import re

from Hmod import Hmod


def get_number(line):
    number = line.split('=')[-1].split(';')[0]
    try:
        return int(number)
    except ValueError:
        return float(number)


def get_parameter_value(parameter):
    return parameter.split('=')[-1].replace('"', '').replace("'", "").replace(";", "")


def match_patterns(category, parameter, hmod):
    """
    Check if the file lines match the correct patterns
    :param hmod:
    :param category: The category that will be analyzed
    :param parameter: The file line
    :return:
    """

    category_dict = {
        "species": [['id', 'compartment'], ['val', 'fixed', 'min', 'max', 'isres']],
        "compartments": [['id'], ['val', 'fixed', 'min', 'max', 'isres']],
        "parameters": [['id', 'reaction'], ['val', 'fixed']],
        "ruleAss": [['id', 'val'], []],
        "events": [['id', 'trigger', 'delay', 'var[(][0-9]*[)]'], []],
        "reaction": [['id', 'rate'], []],
        "raterules": [['id', 'val'], ['min', 'max', 'isres']],
    }
    string_parameters = category_dict[category][0]
    numbers_parameters = category_dict[category][1]

    reaction_string = r"^[a-zA-Z0-9\_]*\.reaction\([0-9]*\)\.{reaction_id}=(\"|')\[[a-zA-Z0-9 \/\*\+\-\'\,\"]*\](\"|');$"

    for s in string_parameters:

        pattern_string = rf"^[a-zA-Z0-9\_]*\.{category}\([0-9]*\)\.{s}=(\"|').*(\"|');$"

        match = bool(re.match(pattern_string, parameter))
        if match:
            return True

    for s in numbers_parameters:
        pattern_number = rf"^[a-zA-Z0-9\_]*[.]{category}[(][0-9]*[)][.]{s}=([0-9]*[.])?[0-9]+((E|e)\-[0-9]*)?;$"

        match = bool(re.match(pattern_number, parameter))
        if match:
            return True

    return False


def match_reaction_pattern(line, expected_value):
    reaction_string = fr"^[a-zA-Z0-9\_]*\.reaction\([0-9]*\)\.{expected_value}=(\"|')\[[a-zA-Z0-9 \/\*\+\-\'\,\"\.]*\](\"|');$"

    match = bool(re.match(reaction_string, line))
    if match:
        return True
    return False


def get_parameters_from_list(attributes):
    return [i.split(".")[2].split("=")[0].split("(")[0] for i in attributes]


def get_parameter(line):
    return line.split(".")[2].split("=")[0].split("(")[0]


def get_category_lines(category, lines):
    return [i for i in lines if f".n{category}=" in i or f".{category}(" in i]


def get_category_examples(category):
    examples_dict = {
        "species": "FILENAME.nspecies=4;\n"
                   "FILENAME.species(1).id=\"PM\";\n"
                   "FILENAME.species(1).val=0;\n"
                   "FILENAME.species(1).compartment=\"V\";\n"
                   "FILENAME.species(1).fixed=0;\n"
                   "FILENAME.species(1).min=0;\n"
                   "FILENAME.species(1).max=15;\n"
                   "FILENAME.species(1).isres=1;\n"
                   ".....\n\n",
        "compartments": "Park_SBML.ncompartments=1;\n"
                        "Park_SBML.compartments(1).id=\"V\";"
                        "\nPark_SBML.compartments(1).val=1;\n"
                        "Park_SBML.compartments(1).fixed=0;\n"
                        "Park_SBML.compartments(1).min=0;\n"
                        "Park_SBML.compartments(1).max=15;\n"
                        "Park_SBML.compartments(1).isres=0;\n"
                        ".....\n\n",
        "parameters": "Park_SBML.nparameters=9;\n"
                      "Park_SBML.parameters(1).id=\"D\";\n"
                      "Park_SBML.parameters(1).val=0;\n"
                      "Park_SBML.parameters(1).fixed=0;\n"
                      "Park_SBML.parameters(1).reaction=\"global\";\n"
                      ".....\n\n",
        "ruleAss": "Park_SBML.nruleAss=1;"
                   "Park_SBML.ruleAss(1).id=\"D\";\n"
                   "Park_SBML.ruleAss(1).val=\"Feed / V\";\n"
                   ".....\n\n",
        "events": "Park_SBML.nevents=1;"
                  "Park_SBML.events(1).id=\"Controller\";\n"
                  "Park_SBML.events(1).trigger=\"geq(time, 0)\";\n"
                  "Park_SBML.events(1).delay=\"0\";\n"
                  "Park_SBML.events(1).var(1)=\"Feed\";\n"
                  "Park_SBML.events(1).var(1)="u";\n"
                  ".....\n\n",
        "reaction": "Park_SBML.nreaction=4;\n"
                    "Park_SBML.reaction(1).id=\"rPM\";\n"
                    "Park_SBML.reaction(1).rate=\"vPM * (PT - PM)\";\n"
                    "Park_SBML.reaction(1).rPM=\"['1', '0', '0', '0']\";\n"
                    ".....\n\n",
        "raterules": "Park_SBML.nraterules=1;\n"
                     "Park_SBML.raterules(1).id=\"V\";\n"
                     "Park_SBML.raterules(1).val=\"D * V\";\n"
                     "Park_SBML.raterules(1).min=0;\n"
                     "Park_SBML.raterules(1).max=1.5;\n"
                     "Park_SBML.raterules(1).isres=0;\n"
                     ".....\n\n",

    }

    return examples_dict[category]


def get_current_number(parameter):
    return int(parameter.split("(")[1].split(")")[0])


def check_parameters(correct_parameters, parameters, category, count):
    if sorted(parameters) != sorted(correct_parameters):
        if category == "reaction" and 'id' in parameters and 'rate' in parameters and len(parameters) == 3:
            return True

        # Check if there are any missing parameters
        missing_parameters = [i for i in correct_parameters if i not in parameters]

        if len(missing_parameters) > 0:
            return f"Error in {category} {count + 1} parameters. Parameters are missing: {missing_parameters}\n"
        else:
            return f"Error in {category} {count + 1} parameters. The correct list of parameters is {parameters}\n"
    else:
        return True


def get_value_from_parameter(parameter, lines):
    for i in lines:
        if parameter in i:
            return get_parameter_value(i)


def get_vars_from_event(lines):
    var = [get_parameter_value(i) for i in lines if "var(" in i]
    return var


def add_to_hmod(category, lines, hmod):
    if category == "species":
        hmod.add_specie(get_value_from_parameter('.id=', lines),
                        get_value_from_parameter('.compartment=', lines),
                        get_value_from_parameter('.val=', lines),
                        get_value_from_parameter('.fixed=', lines),
                        get_value_from_parameter('.min=', lines),
                        get_value_from_parameter('.max=', lines),
                        get_value_from_parameter('.isres=', lines),
                        )
    elif category == "compartments":
        hmod.add_compartment(get_value_from_parameter('.id=', lines),
                             get_value_from_parameter('.val=', lines),
                             get_value_from_parameter('.fixed=', lines),
                             get_value_from_parameter('.min=', lines),
                             get_value_from_parameter('.max=', lines),
                             get_value_from_parameter('.isres=', lines),
                             )
    elif category == "parameters":
        hmod.add_parameter(get_value_from_parameter('.id=', lines),
                           get_value_from_parameter('.reaction=', lines),
                           get_value_from_parameter('.val=', lines),
                           get_value_from_parameter('.fixed=', lines),
                           )
    elif category == "ruleAss":
        hmod.add_assignment_rule(get_value_from_parameter('.id=', lines),
                                 get_value_from_parameter('.val=', lines),
                                 )
    elif category == "events":
        var = get_vars_from_event(lines)
        hmod.add_event(get_value_from_parameter('.id=', lines),
                       get_value_from_parameter('.trigger=', lines),
                       get_value_from_parameter('.delay=', lines),
                       var[0],
                       var[1],
                       )
    elif category == "reaction":
        hmod.add_reaction(get_value_from_parameter('.id=', lines),
                          get_value_from_parameter('.rate=', lines),
                          get_value_from_parameter(f".{get_value_from_parameter('.id=', lines)}=", lines),
                          )
    elif category == "raterules":
        hmod.add_rate_rule(get_value_from_parameter('.id=', lines),
                           get_value_from_parameter('.val=', lines),
                           get_value_from_parameter('.min=', lines),
                           get_value_from_parameter('.max=', lines),
                           get_value_from_parameter('.isres=', lines),
                           )


def divide_lines(lines, number):
    return [lines[i:i + number] for i in range(0, len(lines), number)]


def validate_category(category, lines, hmod):
    """
    Checks if the catagory is well writen
    :param hmod:
    :param category: The category of the parameters, i.e. Species, Compartments
    :param lines: The lines in the file
    :return: Bool that represents the validity
    """

    # Get the category lines present in the file
    category_lines = get_category_lines(category, lines)

    # The number of element this category has
    try:
        category_number = int(category_lines[0].split("=")[-1].split(";")[0])
    except Exception:
        return f"Error in n{category}. Please confirm that this line is correctly written."

    if len(category_lines) == 1 and category != "events" and category != "raterules":
        # O nspecies tem de ser 0. so deve ser possivel para eventos e rate rules
        return f"Error in {category}. Cannot have 0 values."
    if category_number == 0 and (category == "events" or category == "raterules"):
        return 0

    parameter_dict = {
        "species": ['id', 'compartment', 'val', 'fixed', 'min', 'max', 'isres'],
        "compartments": ['id', 'val', 'fixed', 'min', 'max', 'isres'],
        "parameters": ['id', 'reaction', 'val', 'fixed'],
        "ruleAss": ['id', 'val'],
        "events": ['id', 'var', 'var', 'trigger', 'delay'],
        "reaction": ['id', 'rate'],
        "raterules": ['id', 'val', 'min', 'max', 'isres'],
    }
    parameter_dict_number = {
        "species": 7,
        "compartments": 6,
        "parameters": 4,
        "ruleAss": 2,
        "events": 5,
        "reaction": 3,
        "raterules": 5,
    }

    # Get the parameters of the category
    parameters = parameter_dict[category]

    # Divide the category into smaller lists, that represent an element
    divided_species = divide_lines(category_lines[1:], parameter_dict_number[category])

    # If the number of elements is different than the one stated
    if len(divided_species) != category_number:
        return f"Error in n{category} value. It does not match with the rest of the {category} values.\n" \
               f"It should be displayed as following:\n" \
               f"{get_category_examples(category)}"

    for count, i in enumerate(divided_species):
        current_specie = list(i)

        # Check if the parameters are present for this category
        correct_parameters = check_parameters(parameters, get_parameters_from_list(current_specie), category, count)
        if correct_parameters != True:
            return correct_parameters

        # Check every line of this category to make sure it is well written
        for parameter in current_specie:
            if not match_patterns(category, parameter, hmod):
                if not (category == "reaction" and "=\"[" in parameter):
                    return f"Error in {category} {count + 1}. Please check line:\n\"{parameter}\"\n"

            # Check if the current number is correct
            if count + 1 != get_current_number(parameter):
                return f"Error in {category} {get_current_number(parameter)}. The number should be {count + 1}"
        add_to_hmod(category, current_specie, hmod)

    return 0


def validate_reactions_values(file_lines, hmod):
    values_lines = [i for i in file_lines if "=\"[" in i]

    for value in values_lines:
        expected_value = hmod.reactions[get_current_number(value)-1].id
        if not match_reaction_pattern(value, expected_value):
            return f"Error in reactions {get_current_number(value)}. The id does not match the values line."

    return 0


def validate_hmod(file_lines):
    hmod = Hmod()

    categories = ["compartments", "species", "parameters", "ruleAss", "events", "reaction", "raterules"]

    for category in categories:
        valid = validate_category(category, file_lines, hmod)
        if valid != 0:
            return valid

    valid = validate_reactions_values(file_lines, hmod)
    if valid != 0:
        return valid

    return hmod.is_valid()
