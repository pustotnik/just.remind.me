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
    along with just.remind.me.  If not, see <https://www.gnu.org/licenses/>.
*/

#ifndef __JUSTREMINDME_APPLICATION_H__
#define __JUSTREMINDME_APPLICATION_H__

#include "boost/utility.hpp"

#include "types.h"

namespace jrm
{

/// Not thread safe
class Application: private boost::noncopyable
{
public:

    Application();
    virtual ~Application();

    int run(const CmdLineArgs& cmdLineArgs);

    /// say to do stop, it's not mean that will stoped after call directly
    void sayStop();

private:

};

} // namespace jrm

#endif // __JUSTREMINDME_APPLICATION_H__
