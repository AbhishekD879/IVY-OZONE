import time
from datetime import datetime, timedelta


def event_to_outcome_in_endpoint(resp_json_event_data):
    selection_ids_list = []
    selection_names_list = []
    event_name = resp_json_event_data.get('name')
    event_id = resp_json_event_data.get('id')
    name_override = resp_json_event_data.get('children')[0].get('market').get('children')[0].get('outcome').get('name')
    default_market_id = resp_json_event_data.get('children')[0].get('market').get('id')
    market_name = resp_json_event_data.get('children')[0].get('market').get('name')
    market_count = len(resp_json_event_data.get('children'))
    selection_id = resp_json_event_data.get('children')[0].get('market').get('children')[0].get('outcome').get('id')
    event_start_time_msg = resp_json_event_data.get('startTime')
    format_start_time_in_microservice_msg = datetime.strptime(event_start_time_msg, "%Y-%m-%dT%H:%M:%SZ")
    is_dst = time.localtime().tm_isdst
    event_start_time = format_start_time_in_microservice_msg + timedelta(hours=is_dst)
    race_type_id = resp_json_event_data.get('typeId')
    for market in resp_json_event_data.get('children'):
        for outcome in market.get('market').get('children'):
            selection_ids_list.append(outcome.get('outcome').get('id'))
            selection_names_list.append(outcome.get('outcome').get('name'))
    all_selection_ids = selection_ids_list
    all_selection_names = selection_names_list
    return {
        'event_name': event_name,
        'event_id': event_id,
        'name_override': name_override,
        'default_market_id': default_market_id,
        'market_name': market_name,
        'market_count': market_count,
        'selection_id': selection_id,
        'event_start_time': event_start_time,
        'race_type_id': race_type_id,
        'all_selection_ids': all_selection_ids,
        'all_selection_names': all_selection_names
    }
