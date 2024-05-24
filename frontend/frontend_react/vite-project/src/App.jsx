import { useState, useEffect } from "react";
import { data } from "./data.js";
//import axios from "axios";
import "./App.css";
// import Api_using_axios from "./Components/Api_using_axios.jsx";
function App() {
  const [search, setSearch] = useState("");
  console.log(search);
  return (
    <>
      <div className="m-auto w3/4">
        <form className="search-container">
          <input
            className="input"
            onChange={(e) => setSearch(e.target.value)}
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <button className="button" type="submit">
            Search
          </button>
        </form>

        <thead className="outer_table">
          <tr>
            <th>id</th>
            <th>image_url</th>
            <th>title</th>
            <th>article_url</th>
            <th>highlight</th>
            <th>time_publish</th>
            <th>category</th>
            <th>date_published</th>
            <th>publisher_name</th>
            <th>detail_content</th>
          </tr>
        </thead>
        <tbody className="outer_table">
          {data.map((item) => (
              <tr>
                <td>{item.id}</td>
                <td>{item.image_url}</td>
                <td>{item.title}</td>
                <td>{item.article_url}</td>
                <td>{item.highlight}</td>
                <td>{item.time_publish}</td>
                <td>{item.category}</td>
                <td>{item.date_published}</td>
                <td>{item.publisher_name}</td>
                <td>{item.detail_content}</td>
              </tr>
            ))}
        </tbody>
      </div>
      {/* < Api_using_axios /> */}
    </>
  );
}

export default App;


