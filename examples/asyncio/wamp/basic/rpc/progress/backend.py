###############################################################################
##
##  Copyright (C) 2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

try:
   import asyncio
except ImportError:
   ## Trollius >= 0.3 was renamed
   import trollius as asyncio

from autobahn.wamp.types import CallOptions, RegisterOptions
from autobahn.asyncio.wamp import ApplicationSession



class Component(ApplicationSession):
   """
   Application component that produces progressive results.
   """

   def onJoin(self, details):

      @asyncio.coroutine
      def longop(n, details = None):
         if details.progress:
            for i in range(n):
               details.progress(i)
               yield from asyncio.sleep(1)
         else:
            yield from asyncio.sleep(1 * n)
         return n

      self.register(longop, 'com.myapp.longop', RegisterOptions(details_arg = 'details'))
