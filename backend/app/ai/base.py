from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def analyze_incident(
        self,
        evidence: dict,
    ) -> dict:
        pass

    @abstractmethod
    def review_deployment(
        self,
        deployment: str,
    ) -> dict:
        pass

    @abstractmethod
    def review_iac(
        self,
        content: str,
        iac_type: str,
    ) -> dict:
        pass