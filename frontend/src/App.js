import './App.css';
import GoogleMap from './components/GoogleMap';
import Header from './components/Header'
import React, { useState, useEffect } from 'react';



function StatCard1({ label, placeholder}) {
  return (
    <div className="stat-card1">
      <div className="stat-line">

        <strong>{label}</strong>
      </div>
      <div>
        <p>Total case: {placeholder}</p>
      </div>
      
    
    </div>
  );
}
function StatCard({ label, number}) {
  return (
    <div className="stat-card">
      <div className="stat-line">

        <strong>{label}</strong>
      </div>
      <ProductTable
        products={[
          { id: 1, name: 'Walc', price: 4.9, stock: 20 },
          { id: 2, name: 'Hilenbrand Lounge', price: 1.9, stock: 32 },
          { id: 3, name: 'Stewart Center', price: 2.4, stock: 12 }
          
        ]}
      />
    </div>
  );
}

var points = [40, 100, 1, 5, 25, 10];
function Sort() {
  points.sort(function(a, b){return b-a});
  console.log(points);
}
const useSortableData = (items, config = null) => {
  const [sortConfig, setSortConfig] = React.useState(config);

  const sortedItems = React.useMemo(() => {
    let sortableItems = [...items];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [items, sortConfig]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (
      sortConfig &&
      sortConfig.key === key &&
      sortConfig.direction === 'ascending'
    ) {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  return { items: sortedItems, requestSort, sortConfig };
};

const ProductTable = (props) => {
  const { items, requestSort, sortConfig } = useSortableData(props.products);
  const getClassNamesFor = (name) => {
    if (!sortConfig) {
      return;
    }
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };
  return (
    <table>
    
      <thead>
        <tr>
          <th>
            Name
          </th>
          <th>
            <button
              type="button"
              onClick={() => requestSort('price')}
              className={getClassNamesFor('price')}
            >
              Price
            </button>
          </th>
          <th>
            <button
              type="button"
              onClick={() => requestSort('stock')}
              className={getClassNamesFor('stock')}
            >
              In Stock
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id}>
            <td>{item.name}</td>
            <td>${item.price}</td>
            <td>{item.stock}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

function App() {
  const [placeholder, setPlaceholder] = useState('Hi');

  useEffect(() => {
    fetch('/hello').then(res => res.json()).then(data => {
      setPlaceholder(data.result);
    });
  }, []);

  return(
    
    <div className="App">
      <Header />
      
      
      <div className = "middle">
        <div className = "dashboard">
          <StatCard1 label="General Information" placeholder={placeholder}/>
          <StatCard label="Monitoring Locations"/>
          
          
          
          
        </div>
        
        <div className="map">
          <GoogleMap />
        </div>
        
        
        
      </div>
        
        

    </div>
    
  );
}

export default App;