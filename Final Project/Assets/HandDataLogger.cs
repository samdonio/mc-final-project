using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;
using UnityEngine.XR.Hands;

public class HandDataLogger : MonoBehaviour
{
    // Start is called before the first frame update
    public XRHand rHand;
    XRHandSubsystem m_HandSubsystem;
    public TextMesh activityText;
    Vector3 pos;
    void Start()
    {
        // activityText.text = "Hello World";
        // activityText = GetComponent<TextMesh>();
        activityText.text = "Oh my god please work";
        pos = new Vector3(0, 0, 0);

        // Set up the hand subsystem
        var handSubsystems = new List<XRHandSubsystem>();
        rHand = GetComponent<XRHand>();
        SubsystemManager.GetSubsystems(handSubsystems);

        for (var i = 0; i < handSubsystems.Count; ++i)
        {
            activityText.text = "This is a test";
            var handSubsystem = handSubsystems[i];
            if (handSubsystem.running)
            {
                activityText.text = "Subsystem is running";
                m_HandSubsystem = handSubsystem;
                activityText.text = "m_subsystem != null => " + (m_HandSubsystem != null).ToString();
                // Why is this break here ?
                break;
            }

            activityText.text = "Made it ouside of break condition";

            // if the handsubsystem is running, it breaks and this is never reached?
        }
        if (m_HandSubsystem != null)
        {
            m_HandSubsystem.updatedHands += OnUpdatedHands;
            activityText.text = "OnUpdatedHands was added";
        }
        else
        {
            activityText.text = "Hand subsystem was null";
        }

        // activityText.text = handSubsystems.Count.ToString();

    }

    // Update is called once per frame


    void OnUpdatedHands(XRHandSubsystem subsystem,
        XRHandSubsystem.UpdateSuccessFlags updateSuccessFlags,
        XRHandSubsystem.UpdateType updateType)
    {
        if (updateType == XRHandSubsystem.UpdateType.Dynamic)
        {
            // for(var i = XRHandJointID.BeginMarker.ToIndex();
            //         i < XRHandJointID.EndMarker.ToIndex(); 
            //         i++)
            // {
            //     var trackingData = hand.GetJoint(XRHandJointIDUtility.FromIndex(i));

            //     if trackingData.TryGetPose(out Pose pose)
            //     {

            //     }
            // }
            var indexTip = 11;
            // IT IS THIS LINE RIGHT HERE OFFICER THIS ONE
            // IS THE ONE THAT IS CAUSING THE CRASH ON STARTUP
            var trackingData = rHand.GetJoint(XRHandJointIDUtility.FromIndex(indexTip));
            activityText.text = "Maybe issue with GetJoint";

            // activityText.text = "TrackingData: " + (trackingData != null).ToString();
            // if (trackingData.TryGetPose(out Pose pose))
            // {
            //     // activityText.text = "x: " + pose.position.x.ToString();
            //     // pos = pose.position;
            //     // activityText.text = sum.ToString();
            // }

        }
    }

    void Update()
    {
        // activityText.text = "Updating correctly";

    }
}
