/*globals jQuery, alert*/
(function ($) {

    'use strict';

    /*
     * Draw the city on the canvas
     */
    function draw(grid, blockSize) {
        var i,
            j,
            c = document.getElementById('canvas').getContext("2d"),
            img;

        for (i = 0; i < grid.length; i += 1) {
            for (j = 0; j < grid[i].length; j += 1) {
                img = document.getElementById(grid[i][j]);
                if (img) {
                    c.drawImage(img, i * blockSize, j * blockSize);
                }
            }
        }
    }

    /*
     * Get a random number between min (inclusive) and max (exclusive) with given precision
     * Default min is 0
     * Default max is 1
     * Default precision is 0
     */
    function random(min, max, precision) {
        min = min || 0;
        max = max || 1;
        precision = precision || 0;
        return Math.floor(Math.pow(10, precision) * Math.random() * (max - min) + min) / Math.pow(10, precision);
    }

    /*
     * Get the distance between two points
     * p1 and p2 must be objects with x and y properties
     */
    function distance(p1, p2) {
        return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
    }

    /*
     * Get the radius of a city regarding its size and the size of the map
     */
    function getRadius(width, height, citySize) {
        return Math.sqrt(width * height * citySize / Math.PI) / 2;
    }

    /*
     * Randomize parameters
     */
    function randomize() {
        var width = random(20, 40),
            height = width + random(-10, 10),

            xPosition = random(0, width),
            yPosition = random(0, height),

            worldType = random(1, 4),
            roadDensity = random(1, Math.floor(width + height / 10)),
            cityNumber = random(1, 5),
            citySize = random(5, 20) / 100,
            river = !!random();

        $('#width').val(width);
        $('#height').val(height);
        $('#x-position').val(xPosition);
        $('#y-position').val(yPosition);
        $('#world-type option[value=' + worldType + ']').attr('selected', true);
        $('#road-density').val(roadDensity);
        $('#city-number').val(cityNumber);
        $('#city-size').val(citySize);
        $('#river').attr('checked', river);
        $('#road-density').attr('disabled', worldType === 3);
    }


    /*
     * Create the grid given the width and the height of the map
     */
    function createGrid(width, height) {
        var i, j, result = [],
            tmp = [];

        for (i = 0; i < width; i += 1) {
            tmp = [];
            for (j = 0; j < height; j += 1) {
                tmp.push('none');
            }
            result.push(tmp);
        }

        return result;
    }

    /*
     * Set the type of the point in the grid
     */
    function setType(grid, x, y, type) {
        if (grid[x][y] === 'none' || type === 'road') {
            if (random(0, 8) === 4 && type !== 'road' && type !== 'water') {
                grid[x][y] = 'tree';
            } else {
                grid[x][y] = type;
            }
        }
    }

    /*
     * Generate a random path along the map
     * Used to generate roads and rivers
     */
    function randomPath(grid, width, height, type, quantity) {
        var i = 0,
            points = [],
            x,
            y,
            dir,
            nextBlock;

        while (i < quantity) {
            // General direction of the path : 0 = vertical, 1 = horizontal
            dir = random(0, 2);

            // Coordinates of the first block (one of the edge of the map)
            if (dir === 0) {
                // Vertical
                x = 0;
                y = random(0, height - 1);
                setType(grid, x, y, type);
                while (x < width - 1 && y > 0 && y < height - 1) {
                    nextBlock = random(0, 9);
                    if (nextBlock >= 0 && nextBlock <= 7) {
                        x = x + 1;
                    } else if (nextBlock === 8) {
                        y = y + 1;
                    } else {
                        y = y - 1;
                    }

                    setType(grid, x, y, type);
                }
            } else {
                // Horizontal
                x = random(0, width);
                y = 0;
                setType(grid, x, y, type);
                while (y < height - 1 && x > 0 && x < width - 1) {
                    nextBlock = random(0, 9);
                    if (nextBlock >= 0 && nextBlock <= 7) {
                        y = y + 1;
                    } else if (nextBlock === 8) {
                        x = x + 1;
                    } else {
                        x = x - 1;
                    }

                    setType(grid, x, y, type);
                }
            }

            i += 1;
        }

        return points;
    }

    /*
     * Generate random centers on the map
     * Used for every round-shaped points of interest (cities, city centers, oasis...)
     */
    function randomCenters(width, height, quantity) {
        var centers = [];

        while (centers.length < quantity) {
            centers.push({
                x: random(0, width),
                y: random(0, height)
            });
        }

        return centers;
    }

    /*
     * Crate a urban city
     */
    function cityGenerator(grid, width, height, roadDensity, cityNumber, citySize, river) {

        var i, j, k, r, point,

            radius = getRadius(width, height, citySize),

            // Generate river
            riverPoint = randomPath(grid, width, height, 'water', river ? 1 : 0),

            // Generate roads
            roadPoint = randomPath(grid, width, height, 'road', roadDensity),

            // Generate cities centers
            cities = randomCenters(width, height, cityNumber);

        // Generate houses
        for (i = 0; i < grid.length; i += 1) {
            for (j = 0; j < grid[i].length; j += 1) {
                for (k = 0; k < cities.length; k += 1) {
                    point = {
                        x: i,
                        y: j
                    };
                    r = random(0, 100);
                    if (distance(point, cities[k]) < radius && r < 80) {
                        setType(grid, i, j, 'building');
                        break;
                    } else if (r < 60) {
                        setType(grid, i, j, 'house');
                        break;
                    }
                }
            }
        }
    }

    /*
     * Create a rural city
     */
    function countryGenerator(grid, width, height, roadDensity, cityNumber, citySize, river) {

        var i, j, k, r, point,

            radius = getRadius(width, height, citySize),

            // Generate river
            riverPoint = randomPath(grid, width, height, 'water', river ? 1 : 0),

            // Generate roads
            roadPoint = randomPath(grid, width, height, 'road', roadDensity),

            // Generate cities centers
            cities = randomCenters(width, height, cityNumber);

        // Generate houses
        for (i = 0; i < grid.length; i += 1) {
            for (j = 0; j < grid[i].length; j += 1) {
                for (k = 0; k < cities.length; k += 1) {
                    point = {
                        x: i,
                        y: j
                    };
                    r = random(0, 3);
                    if (distance(point, cities[k]) < radius && r < 2) {
                        setType(grid, i, j, 'house');
                        break;
                    }
                }
            }
        }
    }

    /*
     * Create a desert city
     */
    function desertGenerator(grid, width, height, cityNumber, citySize, river) {

        var i, j, k, r, point,

            radius = getRadius(width, height, citySize),

            // Generate river
            riverPoint = randomPath(grid, width, height, 'water', river ? 1 : 0),

            // Generate cities centers
            cities = randomCenters(width, height, cityNumber);

        // Generate houses
        for (i = 0; i < grid.length; i += 1) {
            for (j = 0; j < grid[i].length; j += 1) {
                for (k = 0; k < cities.length; k += 1) {
                    point = {
                        x: i,
                        y: j
                    };
                    r = random(0, 3);
                    if (distance(point, cities[k]) < radius && r < 2) {
                        setType(grid, i, j, 'desertHouse');
                        break;
                    }
                }
            }
        }
    }

    /*
     * Submit the parameters form
     */
    function submit() {
        var blockSize = +$('#block-size').val(),

            width = +$('#width').val(),
            height = +$('#height').val(),

            xPosition = +$('#x-position').val(),
            yPosition = +$('#y-position').val(),

            worldType = +$('#world-type option:selected').attr('value'),
            roadDensity = +$('#road-density').val(),
            cityNumber = +$('#city-number').val(),
            citySize = +$('#city-size').val(),
            river = $('#river').prop('checked'),

            // Create grid from map size
            grid = createGrid(width, height);

        if (worldType === 1) {
            cityGenerator(grid, width, height, roadDensity, cityNumber, citySize, river);
        } else if (worldType === 2) {
            countryGenerator(grid, width, height, roadDensity, cityNumber, citySize, river);
        } else if (worldType === 3) {
            desertGenerator(grid, width, height, cityNumber, citySize, river);
        } else {
            alert('Something unexpected happened =( Please retry !');
        }

        $('#parameters .row').css('display', 'none');
        $('#parameters .row:first-child').removeAttr('style');
        $('#canvas').attr('width', blockSize * width);
        $('#canvas').attr('height', blockSize * height);

        draw(grid, blockSize);

        $('#canvas').css('display', 'block');
    }

    /*
     * Submit the parameters form
     */
    $('#submit').click(function () {
        submit();
    });

    /*
     * Randomize the parameters
     */
    $('#randomize').click(function () {
        randomize();
    });

    /*
     * Display parameters form
     */
    $('#toggle').click(function () {
        $('#parameters .row').removeAttr('style');
    });

    /*
     * Disabled or enable road density input regarding selected world type
     */
    $('#world-type').change(function () {
        var worldType = +$('#world-type option:selected').attr('value');
        $('#road-density').attr('disabled', worldType === 3);
    });

}(jQuery));
