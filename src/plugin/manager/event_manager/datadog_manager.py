import logging
import hashlib
from datetime import datetime
from typing import Union


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
            "additional_info": self.get_additional_info(raw_data)
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
    def get_additional_info(raw_data: dict) -> dict:
        return {
            "org_name": raw_data.get("org_name", ""),
            "alert_id": raw_data.get("alert_id", ""),
            "alert_priority": raw_data.get("alert_priority", ""),
            "alert_transition": raw_data.get("alert_transition", ""),
            "alert_scope": raw_data.get("alert_scope", ""),
            "link": raw_data.get("link", ""),
            "email": raw_data.get("email", ""),
            "event_type": raw_data.get("event_type", "")
        }

