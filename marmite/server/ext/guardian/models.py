from datetime import datetime
from dataclasses import dataclass


@dataclass
class GuardianRecipe:
    id: str
    pillarId: str
    sectionId: str
    webPublicationDate: datetime
    headline: str
    shortUrl: str
    lastModified: datetime
    main: str
    thumbnail: str
    bodyText: str
    tags: list
