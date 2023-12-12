# Index

## Introduction

Traditional per-title encoding schemes aim to optimize encoding resolutions to deliver the highest perceptual quality for each representation. However, keeping the encoding time within an acceptable threshold for a smooth user experience is equally important, especially in online streaming applications. In this light, we introduce an encoding latency-aware dynamic resolution encoding scheme (LADRE) for adaptive video streaming applications. LADRE determines the encoding resolution and quantization parameter (qp) for each target bitrate by utilizing a random forest-based prediction model for every video segment based on the spatiotemporal features and the target acceptable latency.


## About LADRE

The primary objective of LADRE is a cVBR encoding scheme with a content-adaptive, JND-aware, online bitrate ladder prediction optimized for adaptive streaming applications.
The set of supported resolutions, target bitrates, the maximum acceptable encoding latency, the maximum quality level, and the target JND are considered as inputs to the scheme.
Moreover, the encoder/codec used, is input to the scheme to ensure that the bitrate ladder is generated for the corresponding encoder.
Based on the video complexity features (extracted by VCA) and the input parameters, bitrate-resolution-qp triples are predicted.
The adjacent points of the bitrate ladder are envisioned to have a perceptual quality difference of one JND.
Although reducing the overall encoding energy consumption and storage needed to store the bitrate ladder representations, LADRE is expected to improve the overall compression efficiency of the bitrate ladder encoding.

LiveVBR is available as an open source library, published under the GPLv3 license.

 - [CLI options](cli.md)

 ![LADRE](https://github.com/PhoenixVideo/LADRE/blob/main/docs/LADRE_implementation.png)
