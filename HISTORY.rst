=======
History
=======

0.11 (unreleased)
-----------------

- Added ignored keywords `AnyOf`, `if`, `else`. They don't make sense in
  Form generation and can't be handled properly with wtforms.
- Add `GenericFormField` and `GenericFormFactory` to handle complex objects.
  It allows us to use `BaseForm` to generate the subfield in a deferred way.
- Add support for local references in object and array types [ponym]
- Add support for default values [ponym]
