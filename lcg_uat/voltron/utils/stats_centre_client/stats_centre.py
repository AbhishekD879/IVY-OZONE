from voltron.utils.helpers import do_request


class StatsCentre(object):
    def __init__(self, stats_centre_url):
        self.stats_centre_url = stats_centre_url

    def get_stats_centre_ids(self, category_id: (int, str), class_id: (int, str), type_id: (int, str)) -> dict:
        """
        Performs 'brcompetitionseason' call to stats centre microservice in order to retrieve sportId / areaId / competitionId
        :param category_id: Category (sport) ID in TI (ex.: 16 - Football)
        :param class_id: Class (country) ID in TI (ex.: 97 - England)
        :param type_id: Type (league) ID in TI (ex.: 442 - Premier League)
        :return: dictionary with data, ex.:
        {
            allCompetitions: [,…]
            allSeasons: [,…]
            areaId: 1
            areaName: "England"
            competitionId: 1
            competitionName: "Premier League"
            sportId: 1
            sportName: "Soccer"
        }
        """
        url = f'https://{self.stats_centre_url}/api/brcompetitionseason/{category_id}/{class_id}/{type_id}'
        resp = do_request(url=url, method='GET')
        return resp

    def get_stats_centre_data(self, category_id: (int, str), class_id: (int, str), type_id: (int, str)) -> list:
        """
        Performs 'seasons' call to stats centre microservice in order to retrieve seasons data
        by providing category/class/league IDs (TI based).
        Use to get league name with "Rankings" / "Standings" tabs on Competitions details page.
        :param category_id: Category (sport) ID in TI (ex.: 16 - Football)
        :param class_id: Class (country) ID in TI (ex.: 97 - England)
        :param type_id: Type (league) ID in TI (ex.: 442 - Premier League)
        :return: list of seasons (dictionaries), or in case of errors - single dictionary
        with 'error' key what describes error
        """
        try:
            ids_resp = self.get_stats_centre_ids(category_id=category_id, class_id=class_id, type_id=type_id)
        except Exception as e:
            ids_resp = {'status': e}
        if all(key in ids_resp for key in ['sportId', 'areaId', 'competitionId']):
            sport_id, area_id, competition_id = ids_resp['sportId'], ids_resp['areaId'], ids_resp['competitionId']
            url = f'https://{self.stats_centre_url}/api/seasons/{sport_id}/{area_id}/{competition_id}'
            try:
                resp = do_request(url=url, method='GET')
            except Exception as e:
                resp = [{'error': e,
                         'id': None}]
            return resp
        else:
            return [{'error': ids_resp.get('status'),
                     'id': None}]
