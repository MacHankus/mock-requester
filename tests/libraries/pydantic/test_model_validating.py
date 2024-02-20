from typing import Any
from typing import Tuple

import pytest
from pydantic import BaseModel
from pydantic_core import ValidationError


class TestWhatModelCanValidate:
    @staticmethod
    def _prepare_model() -> Tuple[Any, Any]:
        class InnerModel(BaseModel):
            a: str
            b: int

        class Model(BaseModel):
            integer: int
            string: str
            obj: InnerModel

        return Model, InnerModel

    def test_should_raise_validation_error_when_validating_instance_of_a_class(self):
        # Pydantic cannot validate class instances
        # Arrange
        # model
        Model, _ = self._prepare_model()

        # instance
        class InnerObject:
            a: str = "a"
            b: int = 1

        class Object:
            integer: int = 1
            string: str = "string"
            obj = InnerObject()

        instance = Object()

        # Act

        with pytest.raises(expected_exception=ValidationError):
            Model.model_validate(instance)

    def test_should_raise_validation_error_when_validating_instance_other_model(self):
        # Pydantic cannot validate class instances
        # Arrange
        # model
        Model, _ = self._prepare_model()

        # other model
        class InnerOtherModel(BaseModel):
            a: str = "a"
            b: int = 1

        class OtherModel(BaseModel):
            integer: int = 1
            string: str = "string"
            obj: InnerOtherModel = InnerOtherModel()

        other_model_instance = OtherModel()

        # Act

        with pytest.raises(expected_exception=ValidationError):
            Model.model_validate(other_model_instance)

    def test_should_succeed_when_validating_instance_of_same_model(self):
        # Pydantic cannot validate class instances
        # Arrange
        # model
        Model, InnerModel = self._prepare_model()

        # same model
        same_model_instance = Model(
            integer=1, string="string", obj=InnerModel(a="a", b=1)
        )

        # Act

        try:
            Model.model_validate(same_model_instance)
        except Exception:
            pytest.fail("Validating raised an error - not expected")
        

    def test_should_succeed_when_validating_correct_dict(self):
        # Pydantic cannot validate class instances
        # Arrange
        # model
        Model, _ = self._prepare_model()

        # dict
        dict_obj = dict(
            integer=1, string="string", obj=dict(a="a", b=1)
        )

        # Act

        try:
            Model.model_validate(dict_obj)
        except Exception:
            pytest.fail("Validating raised an error - not expected")