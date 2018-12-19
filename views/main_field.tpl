
<html>
    <head>
        <meta charset="utf-8" />
        <title>Main try</title>
        <script type="text/javascript" src="/js/jquery-3.3.1.min.js"></script>
        <link href="/css/bootstrap.css" rel="stylesheet">
        <style type="text/css">
            canvas {
                border:0;
                display:block;
                margin:0 auto;
            }
        </style>

    </head>
    <body>
        <script type="text/javascript">
          var $SCRIPT_ROOT = "{{ request.script_name }}";
          var value1 = {{value1}};
          var value2 = {{value2}};
          var value3 = {{value3}};
          var value4 = {{value4}};
          var value5 = {{value5}};
          var curr_x = {{curr_x}};
          var curr_y = {{curr_y}};
        </script>
        <div class="container">
            <div class="row">
                <div class="col-2 p-3 bg-secondary text-white">
                    %if value1 > 0:
                        <h1>Stats:</h1>
                        <span>Value 1: {{value1}}.</span><br/>
                        <span>Value 2: {{value2}}.</span><br/>
                        <span>Value 3: {{value3}}.</span><br/>
                        <span>Value 4: {{value4}}.</span><br/>
                        <span>Value 5: {{value5}}.</span><br/>
                    %else:
                        <h1>You might have died.</h1>
                        <p>How are you?</p>
                    %end
                </div>
                <div class="col-10 p-0 bg-light text-dark">
                    <canvas id="hexmap" width="950" height="656"></canvas>
                </div>
            </div>
        </div>
        <script src="/js/hexagons.js"></script>
    </body>
</html>

