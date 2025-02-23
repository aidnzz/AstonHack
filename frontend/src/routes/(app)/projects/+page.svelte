<header class="header">
  <h1>Projects</h1>
</header>

<div class="content">
    <div class="projects">
        <div class="project">
        <h2>Project 1</h2>
        <p>Project 1 description</p>
        </div>
        <div class="project">
        <h2>Project 2</h2>
        <p>Project 2 description</p>
        </div>
        <div class="project">
        <h2>Project 3</h2>
        <p>Project 3 description</p>
        </div>
    </div>
</div>

<div class="box">
    <div class="box-header">
        <h3 class="box-title">Active Projects</h3>
        <span class="status-badge status-active">7 Projects</span>
    </div>
    <div>Total Budget: </div>
</div>
<div class="box">
    <div class="box-header">
        <h3 class="box-title">Pending Approval</h3>
        <span class="status-badge status-pending">3 Projects</span>
    </div>
    <div>Requested: </div>
</div>

<style>
  .header {
    background-color: #f4f4f4;
    padding: 1rem;
    text-align: center;
  }
  .content {
    display: flex;
    justify-content: center;
    padding: 1rem;
  }
  .projects {
    display: grid;
    width: 100%;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }
  .project {
    background-color: #f4f4f4;
    padding: 1rem;
    border-radius: 5px;
  }
  .box {
    background-color: #f4f4f4;
    padding: 1rem;
    margin: 1rem;
    border-radius: 5px;
  }
  .box-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .box-title {
    margin: 0;
  }
  .status-badge {
    padding: 0.5rem;
    border-radius: 5px;
    color: white;
  }
  .status-active {
    background-color: green;
  }
  .status-pending {
    background-color: orange;
  }

  @media (max-width: 768px) {
    .projects {
      grid-template-columns: 1fr;
    }
  }



</style>