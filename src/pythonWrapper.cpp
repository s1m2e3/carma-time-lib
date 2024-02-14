//Script used to wrap the c++ CarmaClock class in python.
//The names of the functions and their required attributes will be maintained in the wrapped class.

#include <boost/python.hpp>
#include <boost/python/def.hpp>
#include "carma_clock.h"

BOOST_PYTHON_MODULE(carmaClockPython) {
    using namespace boost::python;
    class_<fwha_stol::lib::time::CarmaClock>("CarmaClock", init<bool>())
        .def("nowInSeconds", &fwha_stol::lib::time::CarmaClock::nowInSeconds)
        .def("nowInMilliseconds", &fwha_stol::lib::time::CarmaClock::nowInMilliseconds)
        .def("update", &fwha_stol::lib::time::CarmaClock::update,args("current_time"))
        .def("is_simulation_mode", &fwha_stol::lib::time::CarmaClock::is_simulation_mode)
        .def("wait_for_initialization",&fwha_stol::lib::time::CarmaClock::wait_for_initialization)
        .def("sleep_until",&fwha_stol::lib::time::CarmaClock::sleep_until,args("future_time"))
        .def("sleep_for",&fwha_stol::lib::time::CarmaClock::sleep_for,args("time_to_sleep"));
        // .def_readwrite("_current_time", &fwha_stol::lib::time::CarmaClock::_current_time)
        // .def_readwrite("_is_simulation_mode", &fwha_stol::lib::time::CarmaClock::_is_simulation_mode)
        // .def_readwrite("_is_initialized", &fwha_stol::lib::time::CarmaClock::_is_initialized)
        // .def_readwrite("_initialization_mutex", &fwha_stol::lib::time::CarmaClock::_initialization_mutex)
        // .def_readwrite("_initialization_cv", &fwha_stol::lib::time::CarmaClock::_initialization_cv)
        // .def_readwrite("_sleep_mutex", &fwha_stol::lib::time::CarmaClock::_sleep_mutex)
        // .def_readwrite("_sleep_holder", &fwha_stol::lib::time::CarmaClock::_sleep_holder);
        init_module_carmaClockPython();
}
