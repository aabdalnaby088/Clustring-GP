from pydantic import BaseModel
from typing import List

class Cluster(BaseModel):
    """Represents a single cluster with a name and a list of points."""
    cluster_name: str
    points: List[str]

class ClusterResponse(BaseModel):
    """Represents the response structure containing multiple clusters."""
    clusters: List[Cluster]
