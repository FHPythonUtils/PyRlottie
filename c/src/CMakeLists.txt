
# Add all the source files needed to build the executable


add_executable(${PROJECT_NAME} lottie2img.cpp)
target_link_libraries(${PROJECT_NAME} rlottie)
