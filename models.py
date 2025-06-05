from typing import Optional
from datetime import datetime

class Response:
    def __init__(
        self,
        response_id: Optional[int] = None,
        challenge_id: str = None,
        miner_hotkey: str = None,
        node_id: Optional[int] = None,
        processing_time: Optional[float] = None,
        received_at: datetime = None,
        completed_at: Optional[datetime] = None,
        evaluated: bool = False,
        score: Optional[float] = None,
        evaluated_at: Optional[datetime] = None
    ):
        self.response_id = response_id
        self.challenge_id = challenge_id
        self.miner_hotkey = miner_hotkey
        self.node_id = node_id
        self.processing_time = processing_time
        self.received_at = received_at or datetime.now()
        self.completed_at = completed_at
        self.evaluated = evaluated
        self.score = score
        self.evaluated_at = evaluated_at

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for database operations"""
        return {
            'response_id': self.response_id,
            'challenge_id': self.challenge_id,
            'miner_hotkey': self.miner_hotkey,
            'node_id': self.node_id,
            'processing_time': self.processing_time,
            'received_at': self.received_at.isoformat() if self.received_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'evaluated': self.evaluated,
            'score': self.score,
            'evaluated_at': self.evaluated_at.isoformat() if self.evaluated_at else None
        }

    @classmethod
    def from_db_row(cls, row: tuple) -> 'Response':
        """Create a Response instance from a database row"""
        return cls(
            response_id=row[0],
            challenge_id=row[1],
            miner_hotkey=row[2],
            node_id=row[3],
            processing_time=float(row[4]) if row[4] is not None else None,
            received_at=datetime.fromisoformat(row[5]) if row[5] else None,
            completed_at=datetime.fromisoformat(row[6]) if row[6] else None,
            evaluated=bool(row[7]),
            score=float(row[8]) if row[8] is not None else None,
            evaluated_at=datetime.fromisoformat(row[9]) if row[9] else None
        )

class CodegenResponse(Response):
    def __init__(
        self,
        response_id: Optional[int] = None,
        challenge_id: str = None,
        miner_hotkey: str = None,
        node_id: Optional[int] = None,
        processing_time: Optional[float] = None,
        received_at: datetime = None,
        completed_at: Optional[datetime] = None,
        evaluated: bool = False,
        score: Optional[float] = None,
        evaluated_at: Optional[datetime] = None,
        response_patch: Optional[str] = None
    ):
        super().__init__(
            response_id=response_id,
            challenge_id=challenge_id,
            miner_hotkey=miner_hotkey,
            node_id=node_id,
            processing_time=processing_time,
            received_at=received_at,
            completed_at=completed_at,
            evaluated=evaluated,
            score=score,
            evaluated_at=evaluated_at
        )
        self.response_patch = response_patch

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for database operations"""
        base_dict = super().to_dict()
        base_dict['response_patch'] = self.response_patch
        return base_dict

    @classmethod
    def from_db_row(cls, row: tuple) -> 'CodegenResponse':
        """Create a CodegenResponse instance from a database row"""
        base_response = Response.from_db_row(row[:10])
        return cls(
            response_id=base_response.response_id,
            challenge_id=base_response.challenge_id,
            miner_hotkey=base_response.miner_hotkey,
            node_id=base_response.node_id,
            processing_time=base_response.processing_time,
            received_at=base_response.received_at,
            completed_at=base_response.completed_at,
            evaluated=base_response.evaluated,
            score=base_response.score,
            evaluated_at=base_response.evaluated_at,
            response_patch=row[10]
        )

class RegressionResponse(Response):
    def __init__(
        self,
        response_id: Optional[int] = None,
        challenge_id: str = None,
        miner_hotkey: str = None,
        node_id: Optional[int] = None,
        processing_time: Optional[float] = None,
        received_at: datetime = None,
        completed_at: Optional[datetime] = None,
        evaluated: bool = False,
        score: Optional[float] = None,
        evaluated_at: Optional[datetime] = None,
        response_patch: Optional[str] = None
    ):
        super().__init__(
            response_id=response_id,
            challenge_id=challenge_id,
            miner_hotkey=miner_hotkey,
            node_id=node_id,
            processing_time=processing_time,
            received_at=received_at,
            completed_at=completed_at,
            evaluated=evaluated,
            score=score,
            evaluated_at=evaluated_at
        )
        self.response_patch = response_patch

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for database operations"""
        base_dict = super().to_dict()
        base_dict['response_patch'] = self.response_patch
        return base_dict

    @classmethod
    def from_db_row(cls, row: tuple) -> 'RegressionResponse':
        """Create a RegressionResponse instance from a database row"""
        base_response = Response.from_db_row(row[:10])
        return cls(
            response_id=base_response.response_id,
            challenge_id=base_response.challenge_id,
            miner_hotkey=base_response.miner_hotkey,
            node_id=base_response.node_id,
            processing_time=base_response.processing_time,
            received_at=base_response.received_at,
            completed_at=base_response.completed_at,
            evaluated=base_response.evaluated,
            score=base_response.score,
            evaluated_at=base_response.evaluated_at,
            response_patch=row[10]
        ) 