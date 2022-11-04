class Specie:
    def __init__(
        self, specie_id, compartment, val, fixed, specie_min, specie_max, isres
    ):
        self.id = specie_id
        self.compartment = compartment
        self.val = val
        self.fixed = fixed
        self.min = specie_min
        self.max = specie_max
        self.isres = isres

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Compartment: {self.compartment}\n"
            f"Val: {self.val}\n"
            f"Fixed: {self.fixed}\n"
            f"Min: {self.min}\n"
            f"Max: {self.max}\n"
            f"Isres: {self.isres}\n"
        )


class Compartment:
    def __init__(
        self, compartment_id, val, fixed, compartment_min, compartment_max, isres
    ):
        self.id = compartment_id
        self.val = val
        self.fixed = fixed
        self.min = compartment_min
        self.max = compartment_max
        self.isres = isres

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Val: {self.val}\n"
            f"Fixed: {self.fixed}\n"
            f"Min: {self.min}\n"
            f"Max: {self.max}\n"
            f"Isres: {self.isres}\n"
        )


class Parameter:
    def __init__(self, parameter_id, reaction, val, fixed):
        self.id = parameter_id
        self.reaction = reaction
        self.val = val
        self.fixed = fixed

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Reaction: {self.reaction}\n"
            f"Val: {self.val}\n"
            f"Fixed: {self.fixed}\n"
        )


class AssignmentRule:
    def __init__(self, assignment_rule_id, val):
        self.id = assignment_rule_id
        self.val = val

    def __str__(self):
        return f"ID: {self.id}\n" f"Val: {self.val}\n"


class Event:
    def __init__(self, event_id, trigger, delay, var1, var2):
        self.id = event_id
        self.trigger = trigger
        self.delay = delay
        self.var1 = var1
        self.var2 = var2

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Trigger: {self.trigger}\n"
            f"Delay: {self.delay}\n"
            f"Var1: {self.var1}\n"
            f"Var2: {self.var2}\n"
        )


class Reaction:
    def __init__(self, reaction_id, rate, values):
        self.id = reaction_id
        self.rate = rate
        self.values = values

    def __str__(self):
        return f"ID: {self.id}\n" f"Rate: {self.rate}\n" f"Values: {self.values}\n"


class RateRule:
    def __init__(self, rate_rule_id, val, rate_rule_min, rate_rule_max, isres):
        self.id = rate_rule_id
        self.val = val
        self.min = rate_rule_min
        self.max = rate_rule_max
        self.isres = isres

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Val: {self.val}\n"
            f"Min: {self.min}\n"
            f"Max: {self.max}\n"
            f"Isres: {self.isres}\n"
        )


class Hmod:
    species = []
    compartments = []
    parameters = []
    assignment_rules = []
    events = []
    reactions = []
    rate_rules = []

    def __init__(self):
        self.species = []
        self.compartments = []
        self.parameters = []
        self.assignment_rules = []
        self.events = []
        self.reactions = []
        self.rate_rules = []

    def add_specie(
        self, specie_id, compartment, val, fixed, specie_min, specie_max, isres
    ):
        self.species.append(
            Specie(specie_id, compartment, val, fixed, specie_min, specie_max, isres)
        )

    def add_compartment(
        self, compartment_id, val, fixed, compartment_min, compartment_max, isres
    ):
        self.compartments.append(
            Compartment(
                compartment_id, val, fixed, compartment_min, compartment_max, isres
            )
        )

    def add_parameter(self, parameter_id, reaction, val, fixed):
        self.parameters.append(Parameter(parameter_id, reaction, val, fixed))

    def add_assignment_rule(self, assignment_rule_id, val):
        self.assignment_rules.append(AssignmentRule(assignment_rule_id, val))

    def add_event(self, event_id, trigger, delay, var1, var2):
        self.events.append(Event(event_id, trigger, delay, var1, var2))

    def add_reaction(self, reaction_id, rate, values):
        self.reactions.append(Reaction(reaction_id, rate, values))

    def add_rate_rule(self, rate_rule_id, val, rate_rule_min, rate_rule_max, isres):
        self.rate_rules.append(
            RateRule(rate_rule_id, val, rate_rule_min, rate_rule_max, isres)
        )

    def get_compartment_ids(self):
        return [i.id for i in self.compartments]

    def is_valid(self):
        compartments_ids = self.get_compartment_ids()

        species_compartments = [i.compartment for i in self.species]

        for count, cmp in enumerate(species_compartments):
            if cmp not in compartments_ids:
                return (
                    f"Error in species {count + 1} compartments. "
                    f"Compartment {cmp} is not present in the Compartments definition."
                )

        return 0

    def __str__(self):
        res = "Species: \n\n"

        for count, i in enumerate(self.species):
            res += f"Specie {count+1}:\n"
            res += i.__str__()

        res += "\n\n\nCompartments: \n\n"

        for count, i in enumerate(self.compartments):
            res += f"Compartment {count+1}:\n"
            res += i.__str__()

        res += "\n\n\nParameters: \n\n"

        for count, i in enumerate(self.parameters):
            res += f"Parameter {count+1}:\n"
            res += i.__str__()

        res += "\n\n\nAssignment Rules: \n\n"

        for count, i in enumerate(self.assignment_rules):
            res += f"Assignment Rule {count+1}:\n"
            res += i.__str__()

        res += "\n\n\nEvents: \n\n"

        for count, i in enumerate(self.events):
            res += f"Event {count+1}:\n"
            res += i.__str__()

        res += "\n\n\nReactions: \n\n"

        for count, i in enumerate(self.reactions):
            res += f"Reaction {count+1}:\n"
            res += i.__str__()

        res += "\n\n\nRate Rules: \n\n"

        for count, i in enumerate(self.rate_rules):
            res += f"Rate Rule {count+1}:\n"
            res += i.__str__()

        return res
