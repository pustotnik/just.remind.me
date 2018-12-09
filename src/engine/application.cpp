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

#include <cassert>

//#include "tclap/CmdLine.h"

#include "macros.h"
#include "application.h"

//namespace tclap = TCLAP;

namespace jrm
{

Application::Application()
{
}

Application::~Application()
{
}

int Application::run(const CmdLineArgs& cmdLineArgs)
{
    JRM_UNUSED(cmdLineArgs);

    printf("Application::run\n");
    int exitCode = EXIT_FAILURE;
    return exitCode;
}

void Application::sayStop()
{
}

} // namespace jrm
