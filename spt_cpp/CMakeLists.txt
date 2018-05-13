cmake_minimum_required(VERSION 3.8)
project(spt_cpp)

set(CMAKE_CXX_STANDARD 11)
include_directories(phat/include)
set(SOURCE_FILES
        DiMoSC.cpp)

add_executable(spt_cpp ${SOURCE_FILES})