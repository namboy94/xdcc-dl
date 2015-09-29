cmake_minimum_required(VERSION 3.3)
project(XDCC_Download)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp Objects/Config.cpp Objects/Config.h)
add_executable(XDCC_Download ${SOURCE_FILES})