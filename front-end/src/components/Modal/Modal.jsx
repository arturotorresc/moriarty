import React from "react";
import Modal from 'react-bootstrap/Modal';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import "./style.css";

export function Instructions(props) {
  let show = props.show;
  const handleClose = () => props.setShow(false);
  if (!show) {
    return null
  }
  return (
    <>
      <Modal
        size="lg"
        show={show}
        onHide={handleClose}
        backdrop="static"
        keyboard={false}
        aria-labelledby="example-modal-sizes-title-lg"
      >
        <Modal.Header closeButton>
          <Modal.Title>Instructions</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Accordion defaultActiveKey="0">
            <Card>
              <Card.Header>
                <Accordion.Toggle as={Button} variant="outline-info" eventKey="0">
                  Mission
                </Accordion.Toggle>
              </Card.Header>
              <Accordion.Collapse eventKey="0">
                <Card.Body>
                  Hello Detective, I come to you with unbearable news.<br></br>
                  The president's son has been kidnapped and his whereabouts are unknown. <br></br>
                  We suspect the crime family Moriarty was in charge of the kidnapping, but we don’t know for sure. 
                  That’s why I came to you, we need your help locating the Moriarty family so we can get to the president’s son. 
                  We need your coding abilities. <br></br><br></br>
                  Your mission, if you choose to accept it, starts now.
                </Card.Body>
              </Accordion.Collapse>
            </Card>
            <Card>
              <Card.Header>
                <Accordion.Toggle as={Button} variant="outline-info" eventKey="1">
                  How to do it
                </Accordion.Toggle>
              </Card.Header>
              <Accordion.Collapse eventKey="1">
                <Card.Body>
                <h3 id="stating-a-player">Stating a player</h3>
                <p>At the beginning of the file, state your player’s name as the following:</p>
                <pre>
                  <code className="code">
                    player player_name<span class="hljs-comment">;</span>
                  </code>
                </pre>
                <h3 id="moving-and-jumping">Moving and Jumping</h3>
                <p>Your player operates on a map, you can move and rotate by calling the following functions with your player name.</p>
                <pre>
                  <code className="code">
                    move(<span class="hljs-name">player_name</span>)<span class="hljs-comment">;</span><br></br>
                    rotate(<span class="hljs-name">player_name</span>)<span class="hljs-comment">;</span>
                  </code>
                </pre>
                <p>Your player starts by facing north, and it can only move one step forward at a time.</p>
                <p>There will be obstacles along the way, to surpass them you must jump over them by calling the function jump with your player name.</p>
                <pre>
                  <code className="code">
                    jump(<span class="hljs-name">player_name</span>)<span class="hljs-comment">;</span>
                  </code>
                </pre>
                <h3 id="enemies">Enemies</h3>
                <p>You might encounter enemies along the way agent, that why we have provided you with a gun. 
                To shoot a gun you must call the function &#39;shoot&#39; with your player name:</p>
                <pre>
                  <code className="code">
                    shoot(<span class="hljs-name">player_name</span>)<span class="hljs-comment">;</span>
                  </code>
                </pre>
                <p>But be careful, you can only shoot towards the direction you&#39;re facing, and you must be sure your gun is loaded.
                To check if your gun is loaded, you must call the following function:</p>
                <pre>
                  <code className="code">
                    <span class="hljs-selector-tag">gun_loaded</span>?(player_name);
                  </code>
                </pre>
                <p>If your gun isn&#39;t loaded, you can load it by calling:</p>
                <pre>
                  <code className="code">
                    reload_gun(<span class="hljs-name">player_name</span>)<span class="hljs-comment">;</span>
                  </code>
                </pre>
                <p>But be careful, you can run out of ammo and still have enemies near, be sure not to miss.
                Enemies can be found anywhere on the map. To check if an enemy is facing you, call the following:</p>
                <pre>
                  <code className="code">
                    <span class="hljs-selector-tag">enemy</span>?(player_name);
                </code></pre><p>Each one of this <code className="code">special functions</code> returns a <code className="code">boolean</code> value, stating whether or not the action could be completed.</p>
                <h3 id="speaking">Speaking</h3>
                <p>If your player requires in any way to speak, you must do so like the following:</p>
                <pre>
                  <code className="code">
                    speak<span class="hljs-comment">(player_name, "The thing you wish to speak")</span>;
                  </code>
                </pre>
                </Card.Body>
              </Accordion.Collapse>
            </Card>
            <Card>
              <Card.Header>
                <Accordion.Toggle as={Button} variant="outline-info" eventKey="2">
                  Basics
                </Accordion.Toggle>
              </Card.Header>
              <Accordion.Collapse eventKey="2">
                <Card.Body>
                <h3 id="variables">Variables</h3>
                <p>There are three possible types of variables: integers, booleans and strings. It is also possible to declare one-dimension arrays.</p>
                <pre><code className="code"><span class="hljs-keyword">var</span> i : <span class="hljs-keyword">int</span> = <span class="hljs-number">1</span>;<br></br>
                <span class="hljs-keyword">var</span> b : <span class="hljs-keyword">bool</span><br></br>
                <span class="hljs-keyword">var</span> s : <span class="hljs-keyword">string</span> = <span class="hljs-string">"this is a string"</span>;<br></br>
                <span class="hljs-keyword">var</span> i_array[<span class="hljs-number">10</span>] : <span class="hljs-keyword">int</span>;<br></br>
                </code></pre>
                <h3 id="conditionals">Conditionals</h3>
                <p>You can state whether or not to do something by making use of the conditionals.</p>
                <pre><code className="code">if (<span class="hljs-name">enemy</span>?(<span class="hljs-name">player_name</span>)</code></pre>
                <p>As well as the else and else if statement</p>
                <h3 id="loops">Loops</h3>
                <p>You can also repeat an action over and over again with loops.</p>
                <pre><code className="code">loop(<span class="hljs-keyword">move(player_name))</span></code></pre>
                <h3 id="function-declaration">Function Declaration</h3>
                <p>It is also possible to declare functions. It is very important to remember they must be before the <code >main</code> function. 
                The functions can be void or can have a return type of int, string or bool. They can receive any number of parameters, including whole arrays.</p>
                <pre><code className="code"><span class="hljs-selector-tag">function</span> <span class="hljs-selector-tag">jump_obstacle</span>() : <span class="hljs-selector-tag">void</span></code></pre>
                <p>Every code you want to see executed must be on the main()</p>
                </Card.Body>
              </Accordion.Collapse>
            </Card>
          </Accordion>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-info" onClick={handleClose}>
            I Accept
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}