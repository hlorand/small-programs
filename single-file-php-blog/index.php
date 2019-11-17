<?php // CONFIG --------------------------------------- DESCRIPTION ------------
$cfg["website_title"]    = "Website title";          // The smallest single file
$cfg["color_scheme"]     = "#007DDC";                // PHP blog. Place the blog
$cfg["posts_dir"]        = "./posts";                // content inside /posts
$cfg["posts_per_page"]   = 4;                        // folder. Supports image,
$cfg["post_date_format"] = "Y. m. d.";               // video, audio and text
$cfg["label_nextpage"]   = "Next page &gt;&gt;";     // files. Created by:
$cfg["label_prevpage"]   = "&lt;&lt; Previous page"; // Lorand Horvath, 2016
// --------------------- License: https://creativecommons.org/licenses/by-nc/4.0
$filename = htmlspecialchars(base64_decode($_GET['post']??""));
$title = substr($filename,0,-4);
$single = isset($_GET['post']); ?>

<!doctype html> <html>
<head>
	<title><?=!empty($title) ? $title." | ":""?> <?=$cfg['website_title']?> </title>
	<meta charset="utf-8">
	<style>
    body { font-family: "Helvetica", "Arial", sans-serif;
           line-height: 1.5;  color: #555;
           text-align:justify;  white-space: pre-wrap;
           margin: 0 0 130px 0;  padding: 0; }
    h1 { background-color: <?=$cfg["color_scheme"]?>;
         color: #eee;  text-align: center;
         margin: 0;  padding: 10vh; }
    #content { margin: 0% 20%; }
    @media screen and (max-width: 728px) {
        #content{ margin: 0% 10%; } }
    a { color: <?=$cfg['color_scheme']?>;  text-decoration: none; }
    img { max-width:100%;  border:1px dotted grey; }
	</style>
</head>
<body>
<a href="/"><h1>[ <?=$cfg['website_title']?> ]</h1></a>

<div id="content"> <?php
// DISPLAY A SINGLE POST
function singlepost($filename){ global $cfg;
    $pathtofile =  $cfg['posts_dir'] . "/" . $filename;
    $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
    echo '<a href="?post=' . base64_encode($filename) . '"><h2>[ ' . basename($filename,".".$ext) . ' ]</h2></a>';
    echo "<p>" . date($cfg['post_date_format'], filemtime($pathtofile)) ."</p>";
    $pathtofile = str_replace(array('%3A', '%2F'), '/', rawurlencode($pathtofile));
    
    if( in_array( $ext, array('jpg','jpeg','png','gif','webp') ) ){
        echo '<a href="' . $pathtofile . '" target="_blank"><img src="' . $pathtofile . '"></a>';
    } else if ( in_array( $ext, array('mp4','webm','avi','mpg','mpeg') ) ){
        echo '<video width="100%" controls><source src="' . $pathtofile . '"></video>';
    } else if ( in_array( $ext, array('mp3','ogg','wav') ) ){
        echo '<audio width="100%" controls><source src="' . $pathtofile . '"></audio>';
    } else if ( in_array( $ext, array('pdf','htm','html') ) ){
        echo '<iframe frameBorder="0" width="100%" style="height:70vh" src="' . $pathtofile . '"></iframe>';
    } else if ( in_array( $ext, array('txt') ) ){
         echo "<p>".file_get_contents( rawurldecode($pathtofile) )."</p>";
    } else echo '<a href="' . $pathtofile . '">' . $filename . '</a>';
}
if( $single ){ singlepost($filename); die("</div></body></html>"); }

// GET ALL POSTS
if( empty( $posts = glob($cfg['posts_dir'].'/*.*') ) ) { die(); }
usort( $posts, function($a, $b) { return filemtime($a) < filemtime($b); } );

// PAGING
$lastpage = floor(count($posts)/$cfg['posts_per_page']-0.01);
$page = isset($_GET["page"]) ? (int)$_GET["page"] : 0;

// POSTLOOP
foreach($posts as $index=>$p)
    if( $index>=$page*$cfg['posts_per_page'] && $index<($page+1)*$cfg['posts_per_page'] )
        singlepost( basename($p) );

if($page > 0 && $page <=$lastpage ){ echo "<h2><a style='float:left;' href='?page=" . ($page-1) . "'>" . $cfg['label_prevpage'] . "</a></h2>"; }
if($page >= 0 && $page <$lastpage ){ echo "<h2><a style='float:right;' href='?page=" . ($page+1) . "'>" . $cfg['label_nextpage'] . "</a></h2>"; }
?> </div></body></html>