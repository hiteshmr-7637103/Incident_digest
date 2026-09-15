function Navbar () {
    return (
        <nav>
            <ul>
                <li><a href="/">Dashboard</a></li>
                <li><a href="/incidents">Incident overview</a></li>
                <li><a href="/clusters">Clusters</a></li>
                <li><a href="/settings">Settings</a></li>
            </ul>
        </nav>
    );
}

export default Navbar;