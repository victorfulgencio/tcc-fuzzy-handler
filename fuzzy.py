import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyClassifier:

    def __init__(self):
        self.__set_fuzzy_sets()
        self.__set_membership_functions()
        self.__set_fuzzy_rules()

    def __set_fuzzy_sets(self):
        self.cost = ctrl.Antecedent(np.arange(5, 501, 0.1), 'Custo')
        self.service = ctrl.Antecedent(np.arange(0, 501, 1), 'Plano Dados')
        self.city_coverage = ctrl.Antecedent(np.arange(0, 101, 0.001), 'Cobertura Total da Cidade')
        self.most_valuable_areas_coverage = ctrl.Antecedent(np.arange(0, 101, 0.001), 'Cobertura das Áreas Destacadas')
        self.claimed_issues = ctrl.Antecedent(np.arange(0, 1000, 1), 'Reclamações/acesso')
        self.final_rating = ctrl.Consequent(np.arange(0, 11, 0.5), 'Nota Final')

    def __set_membership_functions(self):
        self.city_coverage.automf(5)
        self.most_valuable_areas_coverage.automf(5)
        self.service.automf(5)
        self.final_rating.automf(5)

        self.cost['very_expensive'] = fuzz.trimf(self.cost.universe, [255, 500, 500])
        self.cost['normal_expensive'] = fuzz.trimf(self.cost.universe, [125, 190, 255])
        self.cost['average'] = fuzz.trimf(self.cost.universe, [75, 100, 125])
        self.cost['normal_cheap'] = fuzz.trimf(self.cost.universe, [30, 50, 75])
        self.cost['very_cheap'] = fuzz.trimf(self.cost.universe, [5, 5, 30])

        self.claimed_issues['very_high'] = fuzz.trimf(self.claimed_issues.universe, [700, 1000, 1000])
        self.claimed_issues['normal_high'] = fuzz.trimf(self.claimed_issues.universe, [500, 600, 700])
        self.claimed_issues['average'] = fuzz.trimf(self.claimed_issues.universe, [300, 400, 500])
        self.claimed_issues['normal_low'] = fuzz.trimf(self.claimed_issues.universe, [100, 200, 300])
        self.claimed_issues['very_low'] = fuzz.trimf(self.claimed_issues.universe, [0, 0, 100])

    def __set_fuzzy_rules(self):
        self.rule1 = ctrl.Rule(self.city_coverage['good'] &
                               self.service['good'] &
                               self.most_valuable_areas_coverage['good'] &
                               self.cost['very_cheap'] &
                               self.claimed_issues['very_low'],
                               self.final_rating['good'])
        self.rule2 = ctrl.Rule(
            (self.city_coverage['decent'] &
             self.service['decent'] &
             self.most_valuable_areas_coverage['decent'] &
             self.cost['normal_cheap'] &
             self.claimed_issues['normal_low']
             ) |
            (self.most_valuable_areas_coverage['good'] &
             self.city_coverage['decent']
             ), self.final_rating['decent'])

        self.rule3 = ctrl.Rule(self.city_coverage['average'] &
                               self.service['average'] &
                               self.most_valuable_areas_coverage['average'] &
                               self.cost['average'] &
                               self.claimed_issues['average'],
                               self.final_rating['average'])

        self.rule4 = ctrl.Rule(self.city_coverage['mediocre'] &
                               self.service['mediocre'] &
                               self.most_valuable_areas_coverage['mediocre'] &
                               self.cost['normal_expensive'] &
                               self.claimed_issues['normal_high'],
                               self.final_rating['mediocre'])

        self.rule5 = ctrl.Rule(self.city_coverage['poor'] &
                               self.service['poor'] &
                               self.most_valuable_areas_coverage['poor'] &
                               self.cost['very_expensive'] &
                               self.claimed_issues['very_high'],
                               self.final_rating['mediocre'])

    def get_result_for(self, city_coverage, most_valuable_areas_coverage, cost, service, claimed_issues):
        """Get final_rating<numeric> from input city_coverage, and other params"""

        mobile_operator_ctrl = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3, self.rule4, self.rule5])
        mobile_operator = ctrl.ControlSystemSimulation(mobile_operator_ctrl)

        mobile_operator.input['Cobertura Total da Cidade'] = city_coverage
        mobile_operator.input['Cobertura das Áreas Destacadas'] = most_valuable_areas_coverage
        mobile_operator.input['Custo'] = cost
        mobile_operator.input['Plano Dados'] = service
        mobile_operator.input['Reclamações/acesso'] = claimed_issues

        mobile_operator.compute()
        return mobile_operator.output['Nota Final']
