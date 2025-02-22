

<header class="header">
        <div class="header-content">
            <h1>Budget Planner</h1>
            <div class="profile">
                <div class="dp">
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        <div class="budget">
            <h2>Your Budget</h2>
            <div class="budget-value">0</div>
            <div class="Allocated">Allocated</div>
                <div class="budget-value">0</div>
            <div class="Available">Available</div>
                <div class="budget-value">0</div>
            <div class="budget-income">
                <div class="budget-income-text">Income</div>
                <div class="budget-income-value">+0.00</div>
            </div>
            <div class="budget-expenses">
                <div class="budget-expenses-text">Expenses</div>
                <div class="budget-expenses-value">-0.00</div>
            </div>
        </div>
        <div class="income"></div>
        <div class="expenses"></div>
    </div>

    <div class="container">
        <div class="box">
            <h2>Budget Priorities</h2>
            <button class="add-category">Add Category</button>
        </div>
        <ul class="categories">
            <div class="box">
                <li class="category">
                    <div class="category-name">Category 1</div>
                    <div class="category-amount">0.00</div>
                    <div class="category-delete">
                        <button class="category-delete-button">Delete</button>
                    </div>
                </li>
                <li class="category">
                    <div class="category-name">Category 2</div>
                    <div class="category-amount">0.00</div>
                    <div class="category-delete">
                        <button class="category-delete-button">Delete</button>
                    </div>
                </li>
                <li class="category">
                    <div class="category-name">Category 3</div>
                    <div class="category-amount">0.00</div>
                    <div class="category-delete">
                        <button class="category-delete-button">Delete</button>
                    </div>
                </li>
                <li class="category">
                    <div class="category-name">Category 4</div>
                    <div class="category-amount">0.00</div>
                    <div class="category-delete">
                        <button class="category-delete-button">Delete</button>
                    </div>
                </li>
        </ul>
    </div>

<style>
    .container{
        display: flex;
        justify-content: space-between;
    }

    .budget {
        width: 30%;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }

    h1 {
        font-size: 2rem;
        margin-bottom: 20px;
    }

    .budget h2 {
        font-size: 1.5rem;
        margin-bottom: 20px;
    }

    .budget-value {
        font-size: 2rem;
        margin-bottom: 20px;
    }

    .budget-income, .budget-expenses {
        margin-bottom: 20px;
    }

    .budget-income-text, .budget-expenses-text {
        font-size: 1.2rem;
        margin-bottom: 10px;
    }

    .budget-income-value, .budget-expenses-value {
        font-size: 1.5rem;
    }

    .income, .expenses {
        width: 65%;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }

    .box {
        width: 30%;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }

    .box h2 {
        font-size: 1.5rem;
        margin-bottom: 20px;
    }

    .add-category {
        background-color: #f9f9f9;
        border: 1px solid #000;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
    }

    .categories {
        width: 65%;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }

    .category {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .category-name, .category-amount {
        font-size: 1.2rem;
    }

    .category-delete {
        display: flex;
        align-items: center;
    }

    .category-delete-button {
        background-color: #f9f9f9;
        border: 1px solid #000;
        padding: 5px;
        border-radius: 5px;
        cursor: pointer;
    }

    .category-delete-button:hover {
        background-color: #000;
        color: #fff;
    }

    .profile {
        display: flex;
        align-items: center;
    }

    .dp {
        width: 50px;
        height: 50px;
        background-color: #000;
        border-radius: 50%;
    }

    .header {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header h1 {
        font-size: 2rem;
    }

    

</style>
