import logging
from datetime import datetime

from spaceone.core.manager import BaseManager
from spaceone.core import utils
from plugin.error import *

_LOGGER = logging.getLogger("spaceone")


class DataDogManager(BaseManager):

    def parse(self, raw_data: dict) -> dict:
        """

        :param raw_data: dict
        :return EventResponse: {
           "results": EventResponse
        }
        """
        results = []
        _LOGGER.debug(f"[DataDogManager] data => {raw_data}")
        event: dict = {
            "event_key": raw_data.get("event_key"),
            "event_type": self.get_event_type(raw_data.get("event_type", "")),
            "severity": self.get_severity(raw_data.get("severity", "")),
            "title": raw_data.get("title", ""),
            "rule": raw_data.get("rule", ""),
            "image_url": raw_data.get("image_url", ""),
            "resource": self.get_resource(raw_data.get("resource", {})),
            "account": "",
            "description": raw_data.get("description", ""),
            "occurred_at": self.get_occured_at(raw_data.get("occured_at", "")),
            "additional_info": self.get_additional_info(raw_data.get("additional_info", {}))
        }
        results.append(event)
        _LOGGER.debug(f"[DataDogManager] parse : {event}")

        return {
            "results": results
        }

    @staticmethod
    def get_event_type(event_type: str) -> str:
        """
        event_state
        - error
        - warning
        - success
        - info

        :param event_type:
        :return:
        - RECOVERY/ALERT
        """
        if event_type == "success":
            return "RECOVERY"
        else:
            return "ALERT"

    @staticmethod
    def get_severity(severity: str) -> str:
        """

        :param severity:
            - error
            - warning
            - success
            - info
        :return:
            - ERROR/INFO
        """
        if severity == "info":
            return "INFO"
        else:
            return "ERROR"

    @staticmethod
    def get_resource(resource: dict) -> dict:
        return {
            "name": resource.get("name", ""),
            "id": resource.get("id", ""),
            "resource_type": resource.get("resource_type", "")
        }

    @staticmethod
    def get_occured_at(occured_at: str) -> str:
        if occured_at == "":
            return utils.datetime_to_iso8601(datetime.utcnow())
        else:
            return utils.datetime_to_iso8601(datetime.utcfromtimestamp(int(occured_at)/1000))

    @staticmethod
    def get_additional_info(additional_info: dict) -> dict:
        return {
            "org_name": additional_info.get("org_name", ""),
            "alert_id": additional_info.get("alert_id", ""),
            "alert_priority": additional_info.get("alert_priority", ""),
            "alert_transition": additional_info.get("alert_transition", ""),
            "alert_scope": additional_info.get("alert_scope", ""),
            "link": additional_info.get("link", ""),
            "email": additional_info.get("email", ""),
            "event_type": additional_info.get("event_type", "")
        }

    @staticmethod
    def make_description(description: str) -> str:
        return description.replace("·", "\n")