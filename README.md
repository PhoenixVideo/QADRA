=================
QADRA
=================

| **Read:** | `Online documentation <https://phoenixvideo.github.io/QADRA/>`_
| **Interact:** | `Report an issue <https://github.com/phoenixvideo/QADRA/issues/new>`_

Quality-Aware Dynamic Resolution Adaptation (QADRA) framework is used to determine the pareto-front (termed as convex-hull in adaptive streaming literature) for adaptive video streaming applications using Versatile Video Coding (VVC). 
Keeping the encoding and decoding times within an acceptable threshold is mandatory for smooth and energy-efficient streaming. 
Hence, QADRA determines the encoding resolution for each target bitrate by maximizing eXtended Peak Signal-to-Noise Ratio (XPSNR) metric while constraining the maximum encoding and/ or decoding time below a threshold.
The primary objective of QADRA is to become the best open-source bitrate ladder estimator which aids in energy-efficient video streaming.

QADRA is available as an open source Python-based framework, published under the GPLv3 license.

Please use the following citation option for this repository:

1. Vignesh V Menon, Amritha Premkumar, Prajit T Rajendran, Adam Wieckowski, Benjamin Bross, Christian Timmerer, and Detlev Marpe. 2024. Energy-efficient Adaptive Video Streaming with Latency-Aware Dynamic Resolution Encoding. In Mile-High Video Conference (MHV ’24), February 11–14, 2024, Denver, CO, USA. ACM, New York, NY, USA, 7 pages. `[https://doi.org/10.1145/3593908.3593942]([https://doi.org/10.1145/3638036.3640801](https://doi.org/10.1145/3593908.3593942)) <https://doi.org/10.1145/3593908.3593942>`_
