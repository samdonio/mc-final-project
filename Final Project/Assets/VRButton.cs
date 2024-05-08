using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class VRButton : MonoBehaviour
{
    // Start is called before the first frame update
    public float deadTime = 0.5f;
    public HandDataLogger trackingFile;

    // public ;

    private bool _deadTimeActive = false;


    public UnityEvent onPressed, onReleased;

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Button" && !_deadTimeActive)
        {
            trackingFile.isTracking = !trackingFile.isTracking;

        }
    }
}
