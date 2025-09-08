import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ScrollView } from 'react-native';
import axios from 'axios';

export default function Home() {
  const [inputs, setInputs] = useState({
    N: '',
    P: '',
    K: '',
    temp: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });

  const [result, setResult] = useState('');

  const handleChange = (name, value) => {
    setInputs({ ...inputs, [name]: value });
  };

  const handleSubmit = async () => {
    try {
      console.log("Sending data:", inputs);
  
      const response = await axios.post('http://192.168.1.6:5000/predict', {
        N: parseFloat(inputs.N),
        P: parseFloat(inputs.P),
        K: parseFloat(inputs.K),
        temp: parseFloat(inputs.temp),
        humidity: parseFloat(inputs.humidity),
        ph: parseFloat(inputs.ph),
        rainfall: parseFloat(inputs.rainfall)
      });
  
      console.log("Received response:", response);
  
      if (response && response.data && response.data.crop) {
        setResult(response.data.crop);
      } else {
        setResult("Unexpected response format");
      }
    } catch (error) {
      console.error("Error from backend:", error.message);
      setResult('Error predicting crop.');
    }
  };
  

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.heading}>Crop Recommendation</Text>
      {["N", "P", "K", "temp", "humidity", "ph", "rainfall"].map((key) => (
        <TextInput
          key={key}
          style={styles.input}
          placeholder={key.toUpperCase()}
          keyboardType="numeric"
          onChangeText={(value) => handleChange(key, value)}
          value={inputs[key]}
        />
      ))}
      <Button title="Predict Crop" onPress={handleSubmit} />
      <Text style={styles.result}>{result && `Recommended Crop: ${result}`}</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f0f4f7',
  },
  heading: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginVertical: 5,
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  result: {
    fontSize: 20,
    color: 'green',
    textAlign: 'center',
    marginTop: 20,
  },
});
