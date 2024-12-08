const socket = new WebSocket('ws://yourserver.com/ws/stocks/');

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const stockElement = document.querySelector(`#stock-${data.stock_id}`);
    const stockValueSpan = stockElement.querySelector(`#stock-value-${data.stock_id}`);
    const percentageChangeSpan = stockElement.querySelector(`#percentage-change-${data.stock_id}`);
    
    stockValueSpan.textContent = data.current_balance.toFixed(2);
    percentageChangeSpan.textContent = `${data.change > 0 ? '+' : ''}${data.change.toFixed(2)}%`;
    percentageChangeSpan.classList.toggle('increase', data.change > 0);
    percentageChangeSpan.classList.toggle('decrease', data.change < 0);
};


// Save state before page unload
window.addEventListener('beforeunload', () => {
    localStorage.setItem('stockState', JSON.stringify({
        stockId,
        stockValue,
        increaseActive,
        lastUpdated: Date.now()
    }));
});

// Load state on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedState = JSON.parse(localStorage.getItem('stockState'));
    if (savedState) {
        stockValue = savedState.stockValue;
        increaseActive = savedState.increaseActive;
        const elapsedTime = Date.now() - savedState.lastUpdated;
        adjustStockForElapsedTime(elapsedTime); // Function to apply missed changes
    }
});
