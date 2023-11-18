import pydantic
# from typing import Optional

#схема данных для создания объявления
class CreateAdvertisement:
    title: str
    description: str

    @pydantic.field_validator('title')
    @classmethod
    def secure_password(cls, v:str) -> str:
        if len(v) < 8:
            raise ValueError(f'Minimal length of password is 8')
        return v

# class PatchAdvertisement(CreateAdvertisement):
#     title: Optional[str]
#     description: Optional[str]