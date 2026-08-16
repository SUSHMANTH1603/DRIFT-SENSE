/**
 * @file registration_engine.hpp
 * @brief DRIFT-SENSE: Production C++ Registration Engine
 *
 * High-performance implementation of the classical registration pipeline
 * with optional Siamese DL fallback via ONNX Runtime.
 *
 * Target performance:
 *   - Classical path: < 50 ms p95
 *   - With DL fallback: < 150 ms p95
 *   - Memory: < 512 MB
 */

#pragma once

#include <memory>
#include <string>
#include <vector>

#include <opencv2/core.hpp>

namespace drift_sense {

/**
 * @brief Failure codes from the failure taxonomy (Section 19).
 */
enum class FailureCode {
    F0_UNKNOWN = 0,
    F1_PERIODIC_ALIAS,
    F2_EXCESSIVE_NOISE,
    F3_SCALE_MISMATCH,
    F4_ROTATION_MISMATCH,
    F5_BLUR_MISMATCH,
    F6_STRUCTURAL_DEFORMATION,
    F7_LINE_EDGE_ROUGHNESS,
    F8_WEAK_CONTRAST,
    F9_MISSING_FEATURE,
    F10_EDGE_AMBIGUITY,
    F11_DOMAIN_SHIFT,
    F12_CENTER_PRIOR_ERROR,
    F13_SUBPIXEL_FAILURE,
    F14_CONFIDENCE_MISCALIBRATION,
};

/**
 * @brief A registration candidate with location and score.
 */
struct Candidate {
    double x = 0.0;
    double y = 0.0;
    double score = 0.0;
    int alias_cluster_id = -1;
};

/**
 * @brief Registration result output.
 */
struct Result {
    double x = 0.0;
    double y = 0.0;
    double confidence = 0.0;
    FailureCode failure_code = FailureCode::F0_UNKNOWN;
    std::vector<Candidate> top_candidates;
    double latency_ms = 0.0;
    bool dl_fallback_used = false;
};

/**
 * @brief Configuration for the registration engine.
 */
struct Config {
    // Preprocessing
    double clahe_clip_limit = 2.0;
    int clahe_tile_size = 32;

    // Phase correlation
    int coarse_size = 256;
    int top_k_coarse = 20;

    // DT-NCC
    int medium_size = 512;
    int top_k_medium = 5;

    // ECC
    int ecc_max_iterations = 50;
    double ecc_epsilon = 1e-5;

    // Confidence
    double high_confidence_margin = 0.15;
    double ambiguous_margin = 0.05;

    // Threading
    int num_threads = 4;

    // DL fallback
    std::string onnx_model_path;
    bool enable_dl_fallback = false;
};

/**
 * @brief Main registration engine.
 *
 * Implements the classical-first conditional hybrid pipeline.
 */
class RegistrationEngine {
public:
    explicit RegistrationEngine(const Config& config);
    ~RegistrationEngine();

    /**
     * @brief Register a reference image within a search image.
     *
     * @param reference Reference SEM image (1000x1000, CV_8UC1).
     * @param search Search SEM image (1000x1000, CV_8UC1).
     * @return Registration result with (x, y), confidence, and metadata.
     */
    Result registerImages(const cv::Mat& reference, const cv::Mat& search);

private:
    Config config_;
    // TODO: Add pipeline components
    // std::unique_ptr<ClassicalPipeline> classical_;
    // std::unique_ptr<ReferenceCache> ref_cache_;
    // std::unique_ptr<Ort::Session> siamese_session_;  // If ONNX available
};

}  // namespace drift_sense
