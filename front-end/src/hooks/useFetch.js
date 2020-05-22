import axios from "axios";

axios.defaults.baseURL = "http://localhost:4000";

export const useFetch = (url) => {
  const get = (queryParams = "") => {
    return axios
      .get(`${url}${queryParams}`)
      .then((data) => {
        return data;
      })
      .catch((err) => {
        if (err.response) {
          throw err.response;
        } else if (err.request) {
          throw err.request;
        } else {
          throw err.message;
        }
      });
  };

  const post = (data) => {
    return axios
      .post(url, data)
      .then((data) => data)
      .catch((err) => {
        if (err.response) {
          throw err.response;
        } else if (err.request) {
          throw err.request;
        } else {
          throw err.message;
        }
      });
  };

  return {
    get,
    post,
  };
};
