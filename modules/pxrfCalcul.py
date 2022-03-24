"""
Module for pXRF Calculation
"""
import modules.utils as utils
import math


class pxrfCalcul():

    def __init__(self):
        super(pxrfCalcul, self).__init__()

    def is_plag(self, sample_data):
        """
        Verify if data for sample given is plagioclase
        :param sample_data: element values for sample
        :return: True or False
        """
        element_k_verif, element_p_verif, total_verif = False, False, False
        total = 0
        for element in sample_data:
            total += sample_data[element]

        if total > utils.TOTAL_LIMIT:
            total_verif = True
            for element in sample_data:
                if element == utils.ELEMENT_K:
                    if sample_data[element] < utils.ELEMENT_K_LIMIT:
                        element_k_verif = True
                if element == utils.ELEMENT_P:
                    if sample_data[element] < utils.ELEMENT_P_LIMIT:
                        element_p_verif = True

        if total_verif and element_p_verif and element_k_verif:
            return True
        elif total_verif and not element_k_verif:
            if element_p_verif:
                return True
            else:
                return False
        else:
            return False

    def format_data(self, data):
        data_values = data
        sample_to_remove = []
        removed_sample_data = {}
        # Verify if sample has correct data to be a plagioclase else he will be removed
        for sample in data_values:
            if not self.is_plag(data_values[sample]):
                removed_sample_data[sample] = data_values[sample]
                sample_to_remove.append(sample)
        # Remove sample
        for sample in sample_to_remove:
            utils.remove_sample(sample, data_values)
        return data_values

    def extract_elements(self, data):
        """
        Extract Si, Ca, Al value for each sample and create a dictionnary
        :param data: dictionnary of all dataset
        """
        extract_elements = {}
        for sample in data:
            extract_elements[sample] = {}
            for element in data[sample]:
                if element == utils.ELEMENT_SI or element == utils.ELEMENT_AL or element == utils.ELEMENT_CA:
                    extract_elements[sample][element] = data[sample][element]
        return extract_elements

    def calcul_ratios(self, data):
        """
        Calcul Si ans Al ratio for all dataset
        :param data: dataset formated
        :return:
        """
        data_ratio = {}
        for sample in data:
            data_ratio[str(sample)] = {}
            data_ratio[str(sample)][utils.RATIO_SI] = self.calcul_si_ratio(data[sample])
            data_ratio[str(sample)][utils.RATIO_AL] = self.calcul_al_ratio(data[sample])

        return data_ratio

    def calcul_si_ratio(self, sample_data):
        """
        Calcul ratio [Ca/Si]
        :param sample_data: sample element value {Si, Al, Ca}
        :return: ratio in float value
        """
        return sample_data[utils.ELEMENT_CA] / sample_data[utils.ELEMENT_SI]

    def calcul_al_ratio(self, sample_data):
        """
        Calcul ratio [Ca/Al]
        :param sample_data: sample element value {Si, Al, Ca}
        :return: ratio in float value
        """
        return sample_data[utils.ELEMENT_CA] / sample_data[utils.ELEMENT_AL]

    def calcul_an_content(self, data):
        """
        Calcul An Content for all dataset
        :param data: dataset formated
        :return:
        """
        data_an_content = {}
        for sample in data:
            data_an_content[str(sample)] = {}
            data_an_content[str(sample)][utils.AN_CONTENT_RATIO_SI] = self.calcul_an_content_from_si_ratio(
                data[sample][utils.RATIO_SI])
            data_an_content[str(sample)][utils.AN_CONTENT_RATIO_AL] = self.calcul_an_content_from_al_ratio(
                data[sample][utils.RATIO_AL])

        return data_an_content

    def calcul_an_content_from_si_ratio(self, si_ratio):
        """
        Calcul An Content from ratio (Si/Ca)
        :param ratio:
        :return:
        """
        return (utils.COEF_SI_RATIO_A + math.sqrt(
            utils.COEF_SI_RATIO_B + utils.COEF_SI_RATIO_C * si_ratio)) / utils.COEF_SI_RATIO_D

    def calcul_an_content_from_al_ratio(self, al_ratio):
        """
        Calcul An Content from ratio (Si/Ca)
        :param ratio:
        :return:
        """
        return (utils.COEF_AL_RATIO_A + math.sqrt(
            utils.COEF_AL_RATIO_B - utils.COEF_AL_RATIO_C * al_ratio)) / utils.COEF_AL_RATIO_D
