<!DOCTYPE html>
<html>
<head>
    <title>Python Search Engine</title>
</head>
<body>
    <form method="post" action="homepage.php">
        <input type="text" name="query" placeholder="Enter search query" required>
        <input type="submit" value="Search">
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $query = escapeshellarg($_POST['query']);
        $command = escapeshellcmd("./webretrieve.sh retrieve $query") . " 2>&1";
        $output = shell_exec($command);
    
        // Decode the JSON output
        $results = json_decode($output, true);
    
        if (json_last_error() === JSON_ERROR_NONE && !empty($results)) {
            echo "<h2>Search Results:</h2>";
            echo "<ul>";
            foreach ($results as $result) {
                $doc_id = htmlspecialchars($result['doc_id']);
                $url = htmlspecialchars($result['url']);
                $total_weight = htmlspecialchars($result['total_weight']);
                echo "<li>";
                echo "DocID: $doc_id, ";
                echo "Total Weight: $total_weight, ";
                echo "<a href='$url'>$url</a>";
                echo "</li>";
            }
            echo "</ul>";
        } else {
            echo "<p>No results found or error parsing results.</p>";
        }
    }
    
    ?>
</body>
</html>
