/*
    Copyright (c) 2018 Alexander Magola

    This file is part of just.remind.me.

    just.remind.me is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    just.remind.me is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
*/

#ifndef __JUSTREMINDME_TYPES_H__
#define __JUSTREMINDME_TYPES_H__

#ifdef __cplusplus
#  include <cstddef>
#else
#  include <stddef.h>
#endif

#include <memory>
#include <string>
#include <sstream>
#include <vector>
//#include <list>
//#include <map>
//#include <set>

namespace jrm
{
    typedef std::vector<std::string>     CmdLineArgs;

} // namespace jrm

#endif // __JUSTREMINDME_TYPES_H__
