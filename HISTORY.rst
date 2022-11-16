=======
History
=======

0.14 (2022-11-16)
-----------------

- Fixed `Optional` validator for arrays. It was acheived but now providing
  a custom `Optional` drop in replacement, called `NotRequired`.


0.13 (2022-11-09)
-----------------

- Fixed Enum Types


0.12 (2022-08-25)
-----------------

- Added ignored keywords `additionalProperties` as there's no way to
  currently pass these properties along in a meaningful way


0.11
----

- Added ignored keywords `AnyOf`, `if`, `else`. They don't make sense in
  Form generation and can't be handled properly with wtforms.
- Add `GenericFormField` and `GenericFormFactory` to handle complex objects.
  It allows us to use `BaseForm` to generate the subfield in a deferred way.
- Add support for local references in object and array types [ponym]
- Add support for default values [ponym]
