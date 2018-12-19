(function(){
    var canvas = document.getElementById('hexmap');

    var hexHeight,
        hexRadius,
        hexRectangleHeight,
        hexRectangleWidth,
        hexagonAngle = 0.523598776, // 30 degrees in radians
        sideLength = 10,
        boardWidth = 100,
        boardHeight = 100,
        suggestedMoveMap = [],
        moX,
        moY;


    hexHeight = Math.sin(hexagonAngle) * sideLength;
    hexRadius = Math.cos(hexagonAngle) * sideLength;
    hexRectangleHeight = sideLength + 2 * hexHeight;
    hexRectangleWidth = 2 * hexRadius;

    if (canvas.getContext){
        var ctx = canvas.getContext('2d');

        ctx.fillStyle = "#000000";
        ctx.strokeStyle = "#CCCCCC";
        ctx.lineWidth = 1;

        drawBoard(ctx, boardWidth, boardHeight);

        canvas.addEventListener("click", function(eventInfo) {
            var x,
                y,
                hexX,
                hexY,
                screenX,
                screenY,
                rect;

            rect = canvas.getBoundingClientRect();

            x = eventInfo.clientX - rect.left;
            y = eventInfo.clientY - rect.top;

            hexY = Math.floor(y / (hexHeight + sideLength));
            hexX = Math.floor((x - (hexY % 2) * hexRadius) / hexRectangleWidth);

            clearHexagonWithCheck(ctx, moX, moY)
            moX = hexX
            moY = hexY

            screenX = hexX * hexRectangleWidth + ((hexY % 2) * hexRadius);
            screenY = hexY * (hexHeight + sideLength);

            // Check if the mouse's coords are on the board
            if(hexX >= 0 && hexX < boardWidth) {
                if(hexY >= 0 && hexY < boardHeight) {
                    markTemporarely(ctx, screenX, screenY);

                    $.getJSON($SCRIPT_ROOT + '_click_tile', {
                        hy: hexY,
                        hx: hexX
                      }, function(data) {
                        if (suggestedMoveMap !== undefined) {
                            suggestedMoveMap.forEach(function (value) {
                              clearHexagon(ctx, value[0], value[1])
                            });
                        }
                        suggestedMoveMap = data.result;
                        suggestedMoveMap.forEach(function (value) {
                          markHexagon(ctx, value[0], value[1]);
                        });

                      })

                }
            }
        });

        canvas.addEventListener("mousemove", function(eventInfo) {
            var x,
                y,
                hexX,
                hexY,
                screenX,
                screenY,
                rect;

            rect = canvas.getBoundingClientRect();

            x = eventInfo.clientX - rect.left;
            y = eventInfo.clientY - rect.top;

            hexY = Math.floor(y / (hexHeight + sideLength));
            hexX = Math.floor((x - (hexY % 2) * hexRadius) / hexRectangleWidth);

            if (moX!==hexX && moY!==hexY) {
                clearHexagonWithCheck(ctx, moX, moY)
                moX = hexX
                moY = hexY
                screenX = hexX * hexRectangleWidth + ((hexY % 2) * hexRadius);
                screenY = hexY * (hexHeight + sideLength);
                if(hexX >= 0 && hexX < boardWidth) {
                    if(hexY >= 0 && hexY < boardHeight) {
                        ctx.fillStyle = "#000000";
                        drawHexagon(ctx, screenX, screenY);
                    }
                }
            }
        });
    }

    function drawBoard(canvasContext, width, height) {
        for(var x = 0; x < width; ++x) {
            for(var y = 0; y < height; ++y) {
                clearHexagon(canvasContext, x, y)
            }
        }
    }

    function markHexagon(canvasContext, x, y) {
        canvasContext.fillStyle = "#EFEF00";
        drawHexagon(canvasContext,
            x * hexRectangleWidth + ((y % 2) * hexRadius),
            y * (hexHeight + sideLength)
        );
    }

    function markTemporarely(canvasContext, x, y) {
        canvasContext.fillStyle = "#FF0000";
        drawHexagon(canvasContext, x, y);
        setTimeout(function(){
            canvasContext.fillStyle = "#F6F6F6";
            drawHexagon(canvasContext, x, y);
        }, 500);
    }

    function clearHexagonWithCheck(canvasContext, x, y) {
        if (containsSuggestedMoveMap(x, y)) {
            canvasContext.fillStyle = "#EFEF00";
        }
        else {
            canvasContext.fillStyle = "#F6F6F6";
        }
        drawHexagon(canvasContext,
            x * hexRectangleWidth + ((y % 2) * hexRadius),
            y * (hexHeight + sideLength)
        );
    }

    function clearHexagon(canvasContext, x, y) {
        canvasContext.fillStyle = "#F6F6F6";
        drawHexagon(canvasContext,
            x * hexRectangleWidth + ((y % 2) * hexRadius),
            y * (hexHeight + sideLength)
        );
    }

    function drawHexagon(canvasContext, x, y) {
        canvasContext.beginPath();
        canvasContext.moveTo(x + hexRadius, y);
        canvasContext.lineTo(x + hexRectangleWidth, y + hexHeight);
        canvasContext.lineTo(x + hexRectangleWidth, y + hexHeight + sideLength);
        canvasContext.lineTo(x + hexRadius, y + hexRectangleHeight);
        canvasContext.lineTo(x, y + sideLength + hexHeight);
        canvasContext.lineTo(x, y + hexHeight);
        canvasContext.closePath();
        if (isPlayer(x, y)) {
            canvasContext.fillStyle = "#FF00CC";
            canvasContext.fill();
        }
        else {
            canvasContext.fill();
            canvasContext.stroke();
        }
    }

    function isPlayer(x, y) {
        return (x === curr_x && y === curr_y)
    }

    function containsSuggestedMoveMap(x, y) {
        for (ele in suggestedMoveMap) {
            if (suggestedMoveMap[ele][0]===x && suggestedMoveMap[ele][1]===y) {
                return true;
            }
        }
        return false;
    }

})();
