using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Hands;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Controls;

public class FingerTracker : MonoBehaviour
{
    // Start is called before the first frame update
    public XRHand leftHand { get; }
    public XRHand rightHand { get; }

    public TrackedDevice leftHandTrack;
    public TrackedDevice rightHandTrack;

    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Vector3Control leftHandPos = leftHandTrack.devicePosition;
        
    }
}
