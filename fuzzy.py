import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyClassifier:

    def __init__(self):
        self.__set_fuzzy_sets()
        self.__set_membership_functions()
        self.__set_fuzzy_rules()

    def __set_fuzzy_sets(self):
        self.cost = ctrl.Antecedent(np.arange(5, 501, 0.5), 'Custo')
        self.service = ctrl.Antecedent(np.arange(0, 501, 1), 'Plano Dados')

        self.city_coverage2G = ctrl.Antecedent(np.arange(0, 101, 0.001), 'Cobertura Total da Cidade 2g')
        self.city_coverage3G = ctrl.Antecedent(np.arange(0, 101, 0.001), 'Cobertura Total da Cidade 3g')
        self.city_coverage4G = ctrl.Antecedent(np.arange(0, 101, 0.001), 'Cobertura Total da Cidade 4g')

        self.most_valuable_areas_coverage2G = ctrl.Antecedent(np.arange(0, 101, 0.001),
                                                              'Cobertura das Areas Destacadas 2g')
        self.most_valuable_areas_coverage3G = ctrl.Antecedent(np.arange(0, 101, 0.001),
                                                              'Cobertura das Areas Destacadas 3g')
        self.most_valuable_areas_coverage4G = ctrl.Antecedent(np.arange(0, 101, 0.001),
                                                              'Cobertura das Areas Destacadas 4g')

        self.claimed_issues = ctrl.Antecedent(np.arange(0, 1, 0.00001), 'Reclamacoes')
        self.final_rating = ctrl.Consequent(np.arange(0, 11, 0.5), 'Nota Final')

    def __set_membership_functions(self):
        self.city_coverage2G.automf(3)
        self.city_coverage3G.automf(3)
        self.city_coverage4G.automf(3)
        self.most_valuable_areas_coverage2G.automf(3)
        self.most_valuable_areas_coverage3G.automf(3)
        self.most_valuable_areas_coverage4G.automf(3)

        self.cost['very_expensive'] = fuzz.gaussmf(self.cost.universe, 500, 100)
        self.cost['normal_expensive'] = fuzz.gaussmf(self.cost.universe, 200, 30)
        self.cost['average'] = fuzz.gaussmf(self.cost.universe, 120, 50)
        self.cost['normal_cheap'] = fuzz.trimf(self.cost.universe, [30, 50, 75])
        self.cost['very_cheap'] = fuzz.trimf(self.cost.universe, [5, 5, 30])

        self.claimed_issues['high'] = fuzz.trimf(self.claimed_issues.universe, [0.6, 1, 1])
        self.claimed_issues['average'] = fuzz.gaussmf(self.claimed_issues.universe, 0.5, 0.1)
        self.claimed_issues['low'] = fuzz.trimf(self.claimed_issues.universe, [0, 0, 0.4])

        self.final_rating['very_good'] = fuzz.pimf(self.final_rating.universe, 8.3, 10, 11, 11)
        self.final_rating['good'] = fuzz.gaussmf(self.final_rating.universe, 7.5, 1)
        self.final_rating['average'] = fuzz.gaussmf(self.final_rating.universe, 5.5, 1.5)
        self.final_rating['mediocre'] = fuzz.gaussmf(self.final_rating.universe, 3, 0.5)
        self.final_rating['poor'] = fuzz.trimf(self.final_rating.universe, [0, 0, 2.5])

        self.service['high'] = fuzz.pimf(self.service.universe, 100, 500, 1000, 1000)
        self.service['average'] = fuzz.trimf(self.service.universe, [30, 100, 200])
        self.service['low'] = fuzz.sigmf(self.service.universe, 40, -1)

    def __set_fuzzy_rules(self):
        self.rule1 = ctrl.Rule(self.city_coverage4G['good'] &
                               self.most_valuable_areas_coverage4G['good'] &
                               self.most_valuable_areas_coverage3G['good'] &
                               self.service['high'] &
                               (self.cost['very_cheap'] | self.cost['normal_cheap']) &
                               self.claimed_issues['low'],
                               self.final_rating['very_good'])

        self.rule2 = ctrl.Rule(self.city_coverage4G['good'] &
                               self.most_valuable_areas_coverage4G['good'] &
                               self.service['average'] &
                               (self.cost['normal_cheap'] | self.cost['average']) &
                               self.claimed_issues['low'],
                               self.final_rating['very_good'])

        self.rule3 = ctrl.Rule((self.city_coverage4G['average'] &
                                self.most_valuable_areas_coverage4G['average'] &
                                self.most_valuable_areas_coverage3G['average']) |
                               (self.service['average'] &
                                self.cost['average'] &
                                self.claimed_issues['average']),
                               self.final_rating['average'])

        self.rule4 = ctrl.Rule((~self.city_coverage4G['good'] &
                                ~self.city_coverage3G['good'] &
                                self.city_coverage2G['good']) |
                               (~self.most_valuable_areas_coverage4G['good'] &
                                ~self.most_valuable_areas_coverage3G['good'] &
                                self.most_valuable_areas_coverage2G['good']),
                               self.final_rating['mediocre'])

        self.rule5 = ctrl.Rule((self.city_coverage4G['poor'] & self.city_coverage3G['poor']) |
                               (self.most_valuable_areas_coverage4G['poor'] & self.most_valuable_areas_coverage3G['poor']) |
                               self.claimed_issues['high'],
                               self.final_rating['poor'])

    def get_result_for(self, city_coverage2G, city_coverage3G, city_coverage4G, most_valuable_areas_coverage2G,
                       most_valuable_areas_coverage3G, most_valuable_areas_coverage4G, cost, service, claimed_issues):
        """Get final_rating<numeric> from input city_coverage, and other params"""

        mobile_operator_ctrl = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3, self.rule4, self.rule5])
        mobile_operator = ctrl.ControlSystemSimulation(mobile_operator_ctrl)

        mobile_operator.input['Cobertura Total da Cidade 2g'] = city_coverage2G
        mobile_operator.input['Cobertura Total da Cidade 3g'] = city_coverage3G
        mobile_operator.input['Cobertura Total da Cidade 4g'] = city_coverage4G
        mobile_operator.input['Cobertura das Areas Destacadas 2g'] = most_valuable_areas_coverage2G
        mobile_operator.input['Cobertura das Areas Destacadas 3g'] = most_valuable_areas_coverage3G
        mobile_operator.input['Cobertura das Areas Destacadas 4g'] = most_valuable_areas_coverage4G
        mobile_operator.input['Custo'] = cost
        mobile_operator.input['Plano Dados'] = service
        mobile_operator.input['Reclamacoes'] = claimed_issues

        mobile_operator.compute()
        return mobile_operator.output['Nota Final']
