# vim: set fileencoding=utf8:
"""
short module explanation

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
__VERSION__ = "0.1.0"

class Attrdict(dict):
    """Attribute accessiable dictionary"""
    _mutable = True
    def __getattr__(self, name):
        return self[name]
    def __setattr__(self, name, value):
        if not self._mutable:
            raise AttributeError("Cannot overwrite immutable attrdict")
        if not name in dir(self):
            self[name] = value
        else:
            super(Attrdict, self).__setattr__(name, value)
