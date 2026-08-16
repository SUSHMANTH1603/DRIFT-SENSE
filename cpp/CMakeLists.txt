cmake_minimum_required(VERSION 3.18)
project(drift_sense VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Dependencies ---
find_package(OpenCV 4.8 REQUIRED)
find_package(Eigen3 3.4 REQUIRED)

# Optional: ONNX Runtime for DL fallback
find_package(onnxruntime QUIET)

# --- Library ---
add_library(drift_sense_lib
    src/registration_engine.cpp
)

target_include_directories(drift_sense_lib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${OpenCV_INCLUDE_DIRS}
    ${EIGEN3_INCLUDE_DIR}
)

target_link_libraries(drift_sense_lib PUBLIC
    ${OpenCV_LIBS}
    Eigen3::Eigen
)

if(onnxruntime_FOUND)
    target_link_libraries(drift_sense_lib PUBLIC onnxruntime::onnxruntime)
    target_compile_definitions(drift_sense_lib PUBLIC DRIFT_SENSE_HAS_ONNX=1)
endif()

# --- Executable ---
add_executable(drift_sense_cli src/registration_engine.cpp)
target_link_libraries(drift_sense_cli PRIVATE drift_sense_lib)

# --- Tests ---
enable_testing()
# add_subdirectory(tests)
