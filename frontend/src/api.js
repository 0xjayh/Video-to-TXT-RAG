import axios from 'axios';

//create an instance of axios with base url
const api = axios.create({
    baseURL: "http://localhost:8000"
    });

//Export The API Instance
export default api;
