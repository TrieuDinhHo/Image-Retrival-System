# Video Keyframe Extraction Notebook

This notebook implements a multi-algorithm approach to extract representative keyframes from video content. The method combines traditional image processing with machine learning techniques for robust scene detection.

## Key Algorithms & Techniques

### 1. **Blur Detection Filter**
- **Laplacian Variance**: Identifies blurry frames using variance of Laplacian operator
- **Purpose**: Filters out low-quality frames from processing pipeline
- **Implementation**: `filter_blurry()` from low_level_filter module

### 2. **Histogram Analysis**
- **Color Distribution**: Analyzes RGB/HSV histograms between frames
- **Thresholding**: Removes frames with insufficient histogram variation
- **Implementation**: `filter_histogram()` from low_level_filter

### 3. **HOG Feature Extraction**
- **Gradient Analysis**: Captures edge/texture patterns using Histogram of Oriented Gradients
- **Implementation**: `process_hog()` from low_level_filter

### 4. **CNN Embedding Clustering**
- **Feature Extraction**: Uses pre-trained CNN model (from `get_CNN_model()`) to generate frame embeddings
- **Dimensionality Reduction**: StandardScaler and MinMaxScaler for feature normalization
- **Implementation**: `get_CNN_embeddings()` from medium_level_filter

### 5. **Temporal Clustering (DBSCAN)**
- **Density-based Clustering**: Groups visually similar frames using DBSCAN algorithm
- **Benefits**: Handles varying scene lengths automatically
- **Distance Metric**: Cosine similarity for CNN features
- **Parameters**: Adjustable eps and min_samples for cluster granularity

## Workflow Pipeline
1. Video loading and metadata extraction
2. Frame downsampling (configurable stride)
3. Low-level filtering (blur/histogram/HOG)
4. CNN feature extraction
5. DBSCAN clustering for scene detection
6. Keyframe selection from cluster centroids

## Dependencies
```bash
pip install ffmpegcv opencv-python numpy scikit-learn tensorflow