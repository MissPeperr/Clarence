from .database import db_file
from .media import get_media_with_type as get_all_media
from .media import insert as insert_media
from .media import get_single_media
from .media import delete_media
from .media import get_media_with_rec_by
from .media_type import get_all as get_all_types
from .media_type import insert as insert_type
from .recommended_by import insert_rec_by
from .recommended_by import get_all_rec_by
from .recommended_by import check_if_rec_by_exists