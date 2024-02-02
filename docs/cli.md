# Command Line Options

## Logging Options

- `--resultCsv <filename>`

	Write the predicted bitrate ladder to a Comma Separated Values log file. Creates the file if it doesn't already exist. The following parameters are available:

	- `targetBitrate` The target bitrate of the representation
	- `timeLimitEnc` The encoding time constraint used
    - `timeLimitDec` The decoding time constraint used
    - `resolution` The selected optimized encoding resolution
    - `qp` The selected qp for the representation

## Analyzer Configuration

- `--maxEncTime <float>` 

	The encoding time constraint for every representation of the bitrate ladder.

- `--maxDecTime <float>` 

	The decoding time constraint for every representation of the bitrate ladder.

- `--codec <vvenc>` 

	The target encoder used to encode the selected bitrate ladder representations.

- `--rmax <540/720/1080/1440/2160>`
 
	The maximum encoding resolution which may be selected to encode the selected bitrate ladder representations.

- `--maxQuality <double>`
 
	Maximum threshold for the XPSNR of the bitrate ladder representations.

- `--jnd <double>`
 
	Minimum perceptual difference between bitrate ladder representations (in XPSNR).    
