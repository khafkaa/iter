#!/usr/bin/python3

'''Some useful tools for working with iterables and collections.
'''
import re
from itertools import islice
from collections import UserDict


class CustomDict(UserDict):
  '''CustomDict extends the functionality of the built-in
     dictionary class by adding a 'set-ignore' method
     which updates the container if the specified keys are
     not already in the dictionary.
  '''

  def __repr__(self):
    return f"{type(self).__name__}({super().__repr__()})"

  def set(self, assign=True, **kwargs):
    '''Updates the dictionary with the specified values
       if the specified keys aren't already in the container,
       otherwise it ignores the arguments.

       The assign argument determines whether the container
       will be assigned to a variable or just updated in place.
    '''
    for key, value in kwargs.items():
      if key not in self:
        super().__setitem__(key, value)

    if assign is True:
      return self


def chunks(iterable, size):
  '''Yield successive n-sized chunks from an iterable.
  '''
  for i in range(0, len(iterable), size):
    yield iterable[i:i + size]


def flatten(iterable):
  '''Compress a list of nested lists into a single list.
  '''
  for item in iterable:
    if isinstance(item, (list, tuple)):
      yield from flatten(item)
    else:
      yield item


def nth(iterable, index):
  '''Get the nth element of any iterable; 
     pythonic way to extract an element from a generator 
     without having to convert them to lists or resort to using for loops.
  '''
  return next(islice(iterable, index, index + 1))


def fetch(iterable, token):
  '''Designed for parsing tortuous JSON files, fetch is
     a recursive generator that locates the specified JSON key 
     at any nested depth or complexity.

     Fetch returns a generator.

     ARGUMENTS:
         iterable: json file or object; (dict, list):
             A JSON file with any number of nested lists
             and dictionaries.

         token: str:
             The JSON/dictionary key that points to the
             desired data.
  '''
  if isinstance(iterable, dict):
    for key, value in iterable.items():
      if key == token:
        yield iterable[key]
      if isinstance(value, (dict, list)):
        yield from fetch(value, token)

  elif isinstance(iterable, list):
    for item in iterable:
      if isinstance(item, (dict, list)):
        yield from fetch(item, token)


def multisub(characters, string):
  '''Performs several string substitutions on a single pass using
     a dictionary to provide key-replacement_value pairs.

     USAGE:
         multisub({'#': '$', 'Thomas': 'Hank'}, text_to_be_processed)

         The dict key is the character to be replaced;
         The dict value is the replacement character.

     ARGUMENTS:
         characters: dict: The target characters and their
                           substitution values as key-value
                           pairs.

         string: str: The target string upon which the subs will
                     be performed.
  '''
  regex = re.compile("|".join(map(re.escape, characters.keys())))
  return regex.sub(lambda match: characters[match.group(0)], string)


def cleave(string, char, anterior=True):
  '''Cleave off a portion of a string at the first
     occurence of the specified value.

     USAGE:
         cleave(name@gmail.com, '@')
         >>> name

         cleave(name@gmail.com, '@', anterior=False)
         >>> gmail.com

      ARGUMENTS:
          string: str: target of the operation
          char: str: character at which the slice occurs
          anterior: bool: determines which portion of the string to return
  '''
  if char in string:
    pos = string.find(char)
    result = string[:pos] if anterior is True else string[pos + 1:]
    return result
  return string
