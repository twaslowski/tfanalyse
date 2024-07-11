from tfanalyse.change import Change, ChangeAction


def test_diff_two_properties():
    change = Change(
        address="module.foo.bar",
        type="aws_instance",
        name="baz",
        change_action=ChangeAction.UPDATE,
        properties_before={"foo": "bar"},
        properties_after={"foo": "baz"},
    )
    assert change.diff_properties() == {"foo": ("bar", "baz")}


def test_diff_two_properties_with_no_change():
    change = Change(
        address="module.foo.bar",
        type="aws_instance",
        name="baz",
        change_action=ChangeAction.UPDATE,
        properties_before={"foo": "bar"},
        properties_after={"foo": "bar"},
    )
    assert change.diff_properties() == {}


def test_diff_two_properties_with_new_property():
    change = Change(
        address="module.foo.bar",
        type="aws_instance",
        name="baz",
        change_action=ChangeAction.UPDATE,
        properties_before={"foo": "bar"},
        properties_after={"foo": "bar", "baz": "qux"},
    )
    assert change.diff_properties() == {"baz": (None, "qux")}
