cmake_minimum_required(VERSION 3.3)
project(XDCC_Download)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp Objects/Config.cpp Objects/Config.h Helpers/fileHandlers.cpp Helpers/fileHandlers.h Objects/Server.cpp Objects/Server.h Objects/ServerList.cpp Objects/ServerList.h Objects/Channel.cpp Objects/Channel.h Objects/Bot.cpp Objects/Bot.h Objects/Pack.cpp Objects/Pack.h)
add_executable(XDCC_Download ${SOURCE_FILES})