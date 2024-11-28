# IoT Sherlock: Anomaly Sleuth

## Project Overview

IoT Sherlock: Anomaly Sleuth is a sophisticated real-time anomaly detection system for IoT devices, developed over an intensive period of 3 months. This project processes and analyzes massive amounts of network traffic data from various IoT devices to identify potential security threats and malicious activities. Leveraging big data technologies and advanced machine learning algorithms, IoT Sherlock aims to enhance the security posture of IoT ecosystems.

## Problem Statement

The proliferation of IoT devices has introduced unprecedented security challenges. With billions of connected devices generating enormous amounts of data, traditional security measures are often inadequate. IoT Sherlock addresses this critical issue by:

1. Detecting anomalies in IoT network traffic in real-time
2. Identifying potential security breaches, malware infections, or unusual device behavior
3. Providing actionable insights to security teams for rapid response

## Dataset

We utilized the comprehensive IoT-23 dataset, a large-scale collection of network traffic data from various IoT devices.

- **Source**: Stratosphere Laboratory, Czech Technical University in Prague
- **Link**: [IoT-23 Dataset](https://www.stratosphereips.org/datasets-iot23)
- **Size**: Approximately 325 GB
- **Total number of rows**: 325,310,130
- **File format**: Zeek conn.log files

## Dataset Schema

The IoT-23 dataset uses the following schema, based on the Zeek conn.log format:

| Field Name     | Data Type | Description |
|----------------|-----------|-------------|
| ts             | timestamp | Timestamp of the connection |
| uid            | string    | Unique identifier of the connection |
| id.orig_h      | string    | IP address of the originator |
| id.orig_p      | integer   | Port number of the originator |
| id.resp_h      | string    | IP address of the responder |
| id.resp_p      | integer   | Port number of the responder |
| proto          | string    | Transport layer protocol |
| service        | string    | Application layer protocol |
| duration       | double    | Duration of the connection |
| orig_bytes     | integer   | Number of bytes sent by the originator |
| resp_bytes     | integer   | Number of bytes sent by the responder |
| conn_state     | string    | Connection state |
| local_orig     | boolean   | True if the connection originated locally |
| local_resp     | boolean   | True if the connection responded locally |
| missed_bytes   | integer   | Number of missed bytes |
| history        | string    | Connection state history |
| orig_pkts      | integer   | Number of packets sent by the originator |
| orig_ip_bytes  | integer   | Number of IP bytes sent by the originator |
| resp_pkts      | integer   | Number of packets sent by the responder |
| resp_ip_bytes  | integer   | Number of IP bytes sent by the responder |
| tunnel_parents | string    | Tunnel parents (if any) |
| label          | string    | Classification label (Benign/Malicious) |
| detailed_label | string    | Detailed classification label |

This schema provides a comprehensive view of each network connection, including its temporal characteristics, volume of data transferred, and security classification.


## Technologies Used

- **Apache Spark**: For large-scale data processing and machine learning
- **Apache Kafka**: For real-time data streaming and ingestion
- **Python**: Primary programming language
- **Scikit-learn**: For implementing various machine learning algorithms
- **TensorFlow**: For developing and training deep learning models
- **Matplotlib and Seaborn**: For data visualization and result interpretation
- **Dash**: For creating an interactive, real-time dashboard
- **PySpark**: Spark's Python API for distributed computing
- **Pandas**: For efficient data manipulation and analysis
- **NumPy**: For numerical computing and array operations

## Project Steps

1. **Data Preprocessing**: 
   - Cleaned and prepared the massive IoT-23 dataset (325 GB) for analysis
   - Handled missing values, outliers, and data inconsistencies
   - Converted data types and normalized features

2. **Feature Engineering**: 
   - Created relevant features for anomaly detection, including:
     - Bytes ratio (orig_bytes / resp_bytes)
     - Packet ratio (orig_pkts / resp_pkts)
     - Time-based features (e.g., connections per second)
   - Applied feature scaling and encoding techniques

3. **Model Development**: 
   - Implemented and compared various machine learning models:
     - Random Forest
     - Logistic Regression
     - Decision Trees
     - Support Vector Machines
   - Utilized cross-validation for robust model evaluation

4. **Real-time Processing**: 
   - Set up a Kafka-Spark streaming pipeline for real-time data ingestion and processing
   - Implemented windowed operations for time-based analysis

5. **Model Deployment**: 
   - Deployed the best-performing model (Random Forest) for real-time predictions
   - Integrated the model with the Spark streaming pipeline

6. **Anomaly Detection**: 
   - Implemented threshold-based anomaly detection on streaming data
   - Developed a scoring system to rank the severity of detected anomalies

7. **Model Monitoring**: 
   - Developed a system to continuously evaluate model performance
   - Implemented drift detection to identify when model retraining is necessary

8. **Visualization**: 
   - Created a Dash-based dashboard for real-time anomaly visualization
   - Implemented interactive charts and graphs for data exploration

9. **Ensemble Methods**: 
   - Implemented ensemble techniques (bagging, boosting) to improve prediction accuracy
   - Combined predictions from multiple models for robust anomaly detection

## Key Features

- Real-time anomaly detection in IoT network traffic with sub-second latency
- Scalable processing of large-scale IoT data (325 GB+) using Apache Spark
- Interactive dashboard for visualizing anomalies and system performance
- Continuous model monitoring and automated retraining capabilities
- Ensemble methods for improved accuracy and robustness
- Detailed anomaly explanations based on feature importance and SHAP values

## Results

- Achieved 92% accuracy in detecting known attack patterns
- Successfully processed and analyzed over 325 million network traffic records
- Implemented real-time anomaly detection with an average latency of 500 ms
- Reduced false positive rate by 30% compared to baseline methods
- Identified previously unknown attack patterns in the IoT network

## Future Improvements

1. Implement more advanced deep learning models (LSTM, Autoencoders) for anomaly detection
2. Enhance the explanation system using LIME (Local Interpretable Model-agnostic Explanations)
3. Develop a comprehensive API for seamless integration with other security systems
4. Implement automated response mechanisms for critical anomalies
5. Expand the system to handle a wider variety of IoT devices and protocols
6. Incorporate federated learning for privacy-preserving distributed model training
7. Implement a graph-based anomaly detection approach for network-wide analysis


## Acknowledgments

- Stratosphere Laboratory, Czech Technical University in Prague, for providing the IoT-23 dataset
- The Apache Spark and Kafka communities for their excellent documentation and support
- All contributors who have invested their time in helping to improve IoT Sherlock